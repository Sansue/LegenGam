let all_charts = []; // original was {};
let chart_counter = 1;
add_new_viewer(0);
let add_viewer_button = document.getElementById("add_viewer_button");
add_viewer_button.addEventListener("click", ev => {
        ev.preventDefault();
        add_new_viewer(chart_counter);
        chart_counter++;
    }
);

function get_data(i, dataset) {
    if (all_charts[i].Graph != null) {
        all_charts[i].Graph.destroy();
    }

    let formData = new FormData();
    formData.append('element', dataset);

    const request = new Request('get_data/', {
        method: 'POST',
        body: formData
    });

    fetch(request)
        .then(response => response.json())
        .then(result => {
            all_charts[i].all_data = result['stats'];
            //console.log(all_data);
            all_charts[i].chart_types = result['chart_types'];
            all_charts[i].current_dataset = dataset;
            handle_chart_types(i);
            document.getElementById(`numerical_limit_${i}`).max = all_charts[i].all_data.length;
            document.getElementById(`numerical_limit_${i}`).value = all_charts[i].all_data.length;
            document.getElementById(`numerical_limit_text_${i}`).innerHTML = "Maximum elements shown: " + document.getElementById(`numerical_limit_${i}`).value;
            let config = handle_config(i, all_charts[i].all_data);
            all_charts[i].Graph = new Chart(all_charts[i].ctx, config);
            all_charts[i].Graph.update();
        })

}

function handle_config(i, data) {
    document.getElementById(`position_form_${i}`).hidden = true;
    let labels = [];
    let colors = [];
    all_charts[i].chart_colors = generate_random_colors(data.length);
    let datasets = [];
    let dataset = {};
    let options = {};
    all_charts[i].chart_labels = [];
    all_charts[i].chart_data = [];
    for (let color of all_charts[i].chart_colors) {
        colors.push(color.replace("1)", "0.5)"));
    }
    if (all_charts[i].current_dataset === "champs_winrate") {

        for (const [name, winrate] of data) {
            labels.push(name);
            all_charts[i].chart_labels.push(name);
            all_charts[i].chart_data.push(winrate);
        }
        options = {scales: {yAxes: [{ticks: {beginAtZero: true, min: 0, max: 100}}]}};
        dataset['label'] = 'Winrate';
        dataset['data'] = all_charts[i].chart_data;
        dataset['backgroundColor'] = colors;
        dataset['borderColor'] = all_charts[i].chart_colors;
        dataset['borderWidth'] = 1;
        datasets.push(dataset);
    } else if (all_charts[i].current_dataset === "position_stats") {
        labels = ['Winrate', 'KDA', 'Gold', 'Max Time spent living', 'CS', 'Vision Score', 'Level'];
        all_charts[i].chart_labels = labels;
        all_charts[i].chart_data = [];
        datasets = [{
            label: "",
            backgroundColor: 'rgba(54, 162, 235, 0)',
            borderColor: 'rgba(54, 162, 235,0)',
            fillColor: "rgba(220,220,220,0)",
            strokeColor: "rgba(220,220,220,0)",
            pointColor: "rgba(220,220,220,0)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,0)",
            data: []
        }];
        options = {line: {borderWidth: 3}, scale: {ticks: {beginAtZero: true, min: 0, max: 1, display: false}}};
        document.getElementById(`position_form_${i}`).hidden = false;
        document.getElementById(`numerical_limit_${i}`).max = 7;
        document.getElementById(`numerical_limit_${i}`).value = 7;
    } else if (all_charts[i].current_dataset === "cenareo_stats") {
        for (let j = 0; j < all_charts[i].all_data.length; j++) {
            all_charts[i].chart_labels.push(all_charts[i].all_data[j].full_name);
            all_charts[i].chart_data.push(all_charts[i].all_data[j].count);
        }
        labels = all_charts[i].chart_labels;
        options = {maintainAspectRatio: true, legend: {position: "bottom", display: false}};
        dataset['label'] = 'Count';
        dataset['data'] = all_charts[i].chart_data;
        dataset['backgroundColor'] = colors;
        dataset['borderColor'] = all_charts[i].chart_colors;
        datasets.push(dataset);
    }
    //document.getElementById(`data_sort_menu_${i}`).innerHTML += `<option id="${dataset['label']}_sort_button">${dataset['label']}<option>`
    return {type: all_charts[i].chart_types[0], data: {labels: labels, datasets: datasets}, options: options};
}

function generate_random_colors(i) { //generates a list with i random colors in "rgba(x,y,z,a)" form
    let result = [];
    for (let j = 0; j < i; j++) {
        result.push('rgba(' + Math.floor(Math.random() * 255) + ', ' + Math.floor(Math.random() * 255) + ', ' + Math.floor(Math.random() * 255) + ', 1)');
    }
    return result;
}

function handle_chart_types(i) {
    document.getElementById(`graph_type_${i}`).innerHTML = "";
    let options = document.createElement("options");
    for (let chart_type of all_charts[i].chart_types) {
        options.innerHTML += "<a class='btn btn-primary' id='position_" + chart_type + "_button_" + i + "'>" + chart_type + "</a>\n";
    }
    document.getElementById(`graph_type_${i}`).appendChild(options);
}

function handle_type_change(i, new_type, temp) {
    temp.type = new_type;
    if (new_type === 'line') {
        if (all_charts[i].current_dataset === "champs_winrate") {
            temp.options = {scales: {yAxes: [{ticks: {beginAtZero: true, min: 0, max: 100}}]}};
        } else {
            temp.options = {};
        }
        document.getElementById(`dataset_scale_container_${i}`).hidden = false;
        for (let j = 0; j < temp.data.datasets.length; j++) {
            temp.data.datasets[j].fill = false;
            temp.data.datasets[j].tension = 0.1;
            temp.data.datasets[j].borderColor = all_charts[i].chart_colors[j];
            temp.data.datasets[j].backgroundColor = all_charts[i].chart_colors[j].replace("1)", "0.5)");
        }
    } else if (new_type === 'bar') {
        temp.options = {};
        if (all_charts[i].current_dataset === "position_stats") {
            temp.data.datasets = [];
        }
        document.getElementById(`dataset_scale_container_${i}`).hidden = false;
        for (let j = 0; j < temp.data.datasets.length; j++) {
            temp.data.datasets[j].borderColor = all_charts[i].chart_colors;
            temp.data.datasets[j].backgroundColor = [];
            for (let color of all_charts[i].chart_colors) {
                temp.data.datasets[j].backgroundColor.push(color.replace("1)", "0.5)"));
            }
        }
    } else if (new_type === 'pie' || new_type === 'doughnut') {
        temp.options = {};
        document.getElementById(`dataset_scale_container_${i}`).hidden = true;
        for (let j = 0; j < temp.data.datasets.length; j++) {
            temp.hoverOffset = 4;
            temp.data.datasets[j].borderColor = all_charts[i].chart_colors;
            temp.data.datasets[j].backgroundColor = [];
            for (let color of all_charts[i].chart_colors) {
                temp.data.datasets[j].backgroundColor.push(color.replace("1)", "0.5)"));
            }
        }
    } else if (new_type === 'radar') {
        temp.options = {scale: {ticks: {}}};
        document.getElementById(`dataset_scale_container_${i}`).hidden = false;
        for (let j = 0; j < temp.data.datasets.length; j++) {
            temp.data.datasets[j].fill = true;
            temp.data.datasets[j].tension = 0.1;
            temp.data.datasets[j].borderColor = all_charts[i].chart_colors[0];
            temp.data.datasets[j].backgroundColor = all_charts[i].chart_colors[0].replace("1)", "0.2)");
            temp.data.datasets[j].pointBackgroundColor = all_charts[i].chart_colors[0];
        }
    }
    return temp;
}

function handle_sorting(i, order) {
    //console.log(chart_data, chart_labels)
    const intList = all_charts[i].chart_data;
    const stringList = all_charts[i].chart_labels;
    const colorList = all_charts[i].Graph.config.data.datasets[0].backgroundColor;
    const borderColorList = all_charts[i].Graph.config.data.datasets[0].borderColor;
    const combinedList = intList.map((value, index) => ({
        int: value,
        string: stringList[index],
        color: colorList[index],
        borderColor: borderColorList[index]
    }));
    if (order === 'ascending') {
        combinedList.sort((a, b) => a.int - b.int);
    } else {
        combinedList.sort((a, b) => b.int - a.int);
    }
    let sortedIntList = combinedList.map(obj => obj.int); //could do all this shit in the return line, but it's more understandable this way
    let sortedStringList = combinedList.map(obj => obj.string);
    let sortedColorList = combinedList.map(obj => obj.color);
    let sortedBorderColorList = combinedList.map(obj => obj.borderColor);
    return [sortedIntList, sortedStringList, sortedColorList, sortedBorderColorList];
}

function add_new_viewer(i) { // THE ULTIMATE FUNCTION TO RULE THEM ALL

    let viewer = document.createElement("viewer");

    //fetching the html component we need
    let formData = new FormData();
    formData.append('html_type', 'base'); //should change based on what component you want
    formData.append('i', i);
    const request = new Request('get_html/', {
        method: 'POST',
        body: formData
    });

    fetch(request)
        .then(response => response.json())
        .then(result => {
            viewer.innerHTML = result['html'];
            create_viewer_objects(i);
        })
        .catch(error =>{
            console.log(`fetching html element did not work :${error}`);
        })

    document.getElementById("whole_container").appendChild(viewer);
}

function create_viewer_objects(i){
    // Chart creation

    let context = document.getElementById(`chart_${i}`);
    let default_chart = {
    ctx: document.getElementById(`chart_${i}`),
    Graph : new Chart(context, {type: 'bar', data: {labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'], datasets: [{label: 'Example Chart, choose a dataset to change', data: [65, 59, 80, 81, 56, 55], backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(255, 159, 64, 0.2)', 'rgba(255, 205, 86, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(201, 203, 207, 0.2)'], borderColor: ['rgb(255, 99, 132)', 'rgb(255, 159, 64)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)', 'rgb(54, 162, 235)', 'rgb(153, 102, 255)', 'rgb(201, 203, 207)'], borderWidth: 1}]}, options: {scales: {yAxes: [{ticks: {min: 40, max: 85}}]}, legend: {position: "bottom"}}}),
    all_data : [65, 59, 80, 81, 56, 55],
    chart_data : [65, 59, 80, 81, 56, 55],
    chart_labels : ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    chart_types : [],
    chart_colors : ['rgba(255, 99, 132, 0.2)', 'rgba(255, 159, 64, 0.2)', 'rgba(255, 205, 86, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(201, 203, 207, 0.2)'],
    current_dataset : "default",
    current_data_sort : "default"
    };
    all_charts.push(default_chart);

    // add event listeners

    const position_button = document.getElementById(`position_button_${i}`);
    const champion_winrate_button = document.getElementById(`champion_winrate_button_${i}`);
    const cenareo_stats_button = document.getElementById(`cenareo_stats_button_${i}`);
    const graph_type = document.getElementById(`graph_type_${i}`);
    const numerical_limit = document.getElementById(`numerical_limit_${i}`);
    const dataset_min = document.getElementById(`dataset_min_${i}`);
    const dataset_max = document.getElementById(`dataset_max_${i}`);
    //const data_sort_menu = document.getElementById(`data_sort_menu_${i}`);
    const ascending_sort = document.getElementById(`ascending_sort_${i}`);
    const descending_sort = document.getElementById(`descending_sort_${i}`);
    const position_form = document.getElementById(`position_form_${i}`);
    const downloadPdf = document.getElementById(`downloadPdf_${i}`);
    const remove_viewer = document.getElementById(`remove_viewer_${i}`);

    graph_type.addEventListener("click", function (e) {
        e.preventDefault();
        if (e.target !== e.currentTarget) {
            let temp = handle_type_change(i, e.target.innerHTML, all_charts[i].Graph.config);
            all_charts[i].Graph.destroy();
            all_charts[i].Graph = new Chart(all_charts[i].ctx, temp);
            all_charts[i].Graph.update();
        }
    });

    position_form.addEventListener("change", function (e) {
        e.preventDefault();
        if (e.target !== e.currentTarget) {
            if (e.target.id === `Top_${i}`) {
                if (e.target.checked) {
                    all_charts[i].chart_data.push(all_charts[i].all_data.top.top_winrate, all_charts[i].all_data.top.top_kda, all_charts[i].all_data.top.top_gold, all_charts[i].all_data.top.top_timeliving, all_charts[i].all_data.top.top_cs, all_charts[i].all_data.top.top_vision, all_charts[i].all_data.top.top_lvl);
                    all_charts[i].Graph.data.datasets.push({
                        label: 'Top',
                        data: [all_charts[i].all_data.top.top_winrate, all_charts[i].all_data.top.top_kda, all_charts[i].all_data.top.top_gold, all_charts[i].all_data.top.top_timeliving, all_charts[i].all_data.top.top_cs, all_charts[i].all_data.top.top_vision, all_charts[i].all_data.top.top_lvl],
                        backgroundColor: 'rgba(255, 9, 32, 0.2)',
                        borderColor: 'rgb(255, 99, 32)',
                    })
                } else {
                    all_charts[i].Graph.data.datasets = all_charts[i].Graph.data.datasets.filter(elem => elem.label !== "Top");
                    all_charts[i].chart_data = all_charts[i].chart_data.filter(elem => elem[0] !== all_charts[i].all_data.top.top_winrate);
                }
            } else if (e.target.id === `Jungle_${i}`) {
                if (e.target.checked) {
                    all_charts[i].chart_data.push(all_charts[i].all_data.jungle.jungle_winrate, all_charts[i].all_data.jungle.jungle_kda, all_charts[i].all_data.jungle.jungle_gold, all_charts[i].all_data.jungle.jungle_timeliving, all_charts[i].all_data.jungle.jungle_cs, all_charts[i].all_data.jungle.jungle_vision, all_charts[i].all_data.jungle.jungle_lvl);
                    all_charts[i].Graph.data.datasets.push({
                        label: 'Jungle',
                        data: [all_charts[i].all_data.jungle.jungle_winrate, all_charts[i].all_data.jungle.jungle_kda, all_charts[i].all_data.jungle.jungle_gold, all_charts[i].all_data.jungle.jungle_timeliving, all_charts[i].all_data.jungle.jungle_cs, all_charts[i].all_data.jungle.jungle_vision, all_charts[i].all_data.jungle.jungle_lvl],
                        fill: true,
                        backgroundColor: 'rgba(54, 235, 162, 0.2)',
                        borderColor: 'rgb(54, 235, 162)',
                    })
                } else {
                    all_charts[i].Graph.data.datasets = all_charts[i].Graph.data.datasets.filter(elem => elem.label !== "Jungle");
                    all_charts[i].chart_data = all_charts[i].chart_data.filter(elem => elem[0] !== all_charts[i].all_data.top.jungle_winrate);
                }
            } else if (e.target.id === `Mid_${i}`) {
                if (e.target.checked) {
                    all_charts[i].chart_data.push(all_charts[i].all_data.mid.mid_winrate, all_charts[i].all_data.mid.mid_kda, all_charts[i].all_data.mid.mid_gold, all_charts[i].all_data.mid.mid_timeliving, all_charts[i].all_data.mid.mid_cs, all_charts[i].all_data.mid.mid_vision, all_charts[i].all_data.mid.mid_lvl);
                    all_charts[i].Graph.data.datasets.push({
                        label: 'Middle',
                        data: [all_charts[i].all_data.mid.mid_winrate, all_charts[i].all_data.mid.mid_kda, all_charts[i].all_data.mid.mid_gold, all_charts[i].all_data.mid.mid_timeliving, all_charts[i].all_data.mid.mid_cs, all_charts[i].all_data.mid.mid_vision, all_charts[i].all_data.mid.mid_lvl],
                        fill: true,
                        backgroundColor: 'rgba(255, 217, 102, 0.2)',
                        borderColor: 'rgb(255, 217, 102)'
                    })
                } else {
                    all_charts[i].Graph.data.datasets = all_charts[i].Graph.data.datasets.filter(elem => elem.label !== "Middle");
                    all_charts[i].chart_data = all_charts[i].chart_data.filter(elem => elem[0] !== all_charts[i].all_data.top.mid_winrate);
                }
            } else if (e.target.id === `ADC_${i}`) {
                if (e.target.checked) {
                    all_charts[i].chart_data.push(all_charts[i].all_data.adc.adc_winrate, all_charts[i].all_data.adc.adc_kda, all_charts[i].all_data.adc.adc_gold, all_charts[i].all_data.adc.adc_timeliving, all_charts[i].all_data.adc.adc_cs, all_charts[i].all_data.adc.adc_vision, all_charts[i].all_data.adc.adc_lvl);
                    all_charts[i].Graph.data.datasets.push({
                        label: 'ADC',
                        data: [all_charts[i].all_data.adc.adc_winrate, all_charts[i].all_data.adc.adc_kda, all_charts[i].all_data.adc.adc_gold, all_charts[i].all_data.adc.adc_timeliving, all_charts[i].all_data.adc.adc_cs, all_charts[i].all_data.adc.adc_vision, all_charts[i].all_data.adc.adc_lvl],
                        fill: true,
                        backgroundColor: 'rgba(234, 143, 234, 0.2)',
                        borderColor: 'rgb(234, 143, 234)'
                    })
                } else {
                    all_charts[i].Graph.data.datasets = all_charts[i].Graph.data.datasets.filter(elem => elem.label !== "ADC");
                    all_charts[i].chart_data = all_charts[i].chart_data.filter(elem => elem[0] !== all_charts[i].all_data.top.adc_winrate);
                }
            } else if (e.target.id === `Support_${i}`) {
                if (e.target.checked) {
                    all_charts[i].chart_data.push(all_charts[i].all_data.support.support_winrate, all_charts[i].all_data.support.support_kda, all_charts[i].all_data.support.support_gold, all_charts[i].all_data.support.support_timeliving, all_charts[i].all_data.support.support_cs, all_charts[i].all_data.support.support_vision, all_charts[i].all_data.support.support_lvl)
                    all_charts[i].Graph.data.datasets.push({
                        label: 'Support',
                        data: [all_charts[i].all_data.support.support_winrate, all_charts[i].all_data.support.support_kda, all_charts[i].all_data.support.support_gold, all_charts[i].all_data.support.support_timeliving, all_charts[i].all_data.support.support_cs, all_charts[i].all_data.support.support_vision, all_charts[i].all_data.support.support_lvl],
                        fill: true,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgb(54, 162, 235)'
                    })
                } else {
                    all_charts[i].Graph.data.datasets = all_charts[i].Graph.data.datasets.filter(elem => elem.label !== "Support");
                    all_charts[i].chart_data = all_charts[i].chart_data.filter(elem => elem[0] !== all_charts[i].all_data.top.support_winrate);
                }
            } else {
                console.log("error: position form did not find which switch was activated");
            }
            all_charts[i].Graph.update();
        }
    });

    position_button.addEventListener("click", event => {
        event.preventDefault();
        get_data(i, "position_stats")
    });

    champion_winrate_button.addEventListener("click", event => {
        event.preventDefault();
        get_data(i, "champs_winrate")
    });

    cenareo_stats_button.addEventListener("click", event => {
        event.preventDefault();
        get_data(i, "cenareo_stats")
    });

    /* never implemented correctly, the data I had did not display multiple datasets at once
    data_sort_menu.addEventListener("change", event => {
        event.preventDefault();
        all_charts[i].current_data_sort = event.target.value;
    });*/


    ascending_sort.addEventListener("click", event => {
        event.preventDefault();
        [all_charts[i].chart_data, all_charts[i].chart_labels, all_charts[i].Graph.data.datasets[0].backgroundColor, all_charts[i].Graph.data.datasets[0].borderColor] = handle_sorting(i, "ascending");
        all_charts[i].Graph.data.datasets[0].data = all_charts[i].chart_data;
        all_charts[i].Graph.data.labels = all_charts[i].chart_labels;
        all_charts[i].Graph.data.datasets[0].data = all_charts[i].chart_data.slice(0, numerical_limit.value);
        all_charts[i].Graph.data.labels = all_charts[i].chart_labels.slice(0, numerical_limit.value);
        all_charts[i].Graph.update();
    });

    descending_sort.addEventListener("click", event => {
        event.preventDefault();
        [all_charts[i].chart_data, all_charts[i].chart_labels, all_charts[i].Graph.data.datasets[0].backgroundColor, all_charts[i].Graph.data.datasets[0].borderColor] = handle_sorting(i, "descending");
        all_charts[i].Graph.data.datasets[0].data = all_charts[i].chart_data;
        all_charts[i].Graph.data.labels = all_charts[i].chart_labels;
        all_charts[i].Graph.data.datasets[0].data = all_charts[i].chart_data.slice(0, numerical_limit.value);
        all_charts[i].Graph.data.labels = all_charts[i].chart_labels.slice(0, numerical_limit.value);
        all_charts[i].Graph.update();
    });

    numerical_limit.addEventListener("change", event => {
        event.preventDefault();
        document.getElementById(`numerical_limit_text_${i}`).innerHTML = "Maximum elements shown: " + numerical_limit.value;
        all_charts[i].Graph.data.datasets[0].data = all_charts[i].chart_data.slice(0, numerical_limit.value);
        all_charts[i].Graph.data.labels = all_charts[i].chart_labels.slice(0, numerical_limit.value);
        //console.log(all_charts[i].Graph.data.datasets[0].data, all_charts[i].Graph.data.labels);
        all_charts[i].Graph.update();
    });

    dataset_min.addEventListener("change", event => {
        event.preventDefault();
        if (all_charts[i].Graph.config.type === 'radar') { // radar charts have a different scale
            all_charts[i].Graph.options.scale.ticks.min = parseFloat(dataset_min.value);
        } else {
            all_charts[i].Graph.options.scales.yAxes[0].ticks.min = parseFloat(dataset_min.value);
        }
        all_charts[i].Graph.update();
    });

    dataset_max.addEventListener("change", event => {
        event.preventDefault();
        if (all_charts[i].Graph.config.type === 'radar') { // radar charts have a different scale
            all_charts[i].Graph.options.scale.ticks.max = parseFloat(dataset_max.value);
        } else {
            all_charts[i].Graph.options.scales.yAxes[0].ticks.max = parseFloat(dataset_max.value);
        }
        all_charts[i].Graph.update();
    });

     downloadPdf.addEventListener("click", function () {
        const reportPageHeight = 601;
        let canvas_image = document.getElementById(`chart_${i}`).toDataURL("image/png", 1.0);
        let pdf = new jsPDF('l', 'px', [1203 / 1.78, 601]);
        pdf.addImage(canvas_image, 'PNG', 0, 10, 600, 300);
        let labels_text = all_charts[i].chart_labels.toString();
        if (labels_text.length > 35) {
            labels_text = labels_text.substring(0, 35) + "...";
        }
        pdf.setFontSize(40);
        pdf.text(10, reportPageHeight / 1.78 + 30, "Dataset : " + all_charts[i].current_dataset, {horizontalScale: 2, charSpace: 5}); //dataset
        pdf.text(10, reportPageHeight / 1.78 + 70, "Chart type : " + all_charts[i].Graph.config.type); //chart type
        pdf.text(10, reportPageHeight / 1.78 + 110, "Sorted by: " + all_charts[i].current_data_sort); //sorting
        pdf.text(10, reportPageHeight / 1.78 + 150, numerical_limit.value + " elements displayed"); //number of elements
        pdf.text(10, reportPageHeight / 1.78 + 190, "Labels : " + labels_text); //labels
        pdf.text(10, reportPageHeight / 1.78 + 230, "Ratio : 300%");
        pdf.save('chart.pdf');
        });

    remove_viewer.addEventListener("click", function () {
        document.getElementById(`viewer_${i}`).remove();
    });

}