var dummy_data = {
	months: ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
	environmental : [28, 19, 19, 59, 28, 7, 24, 71, 19, 100, 1, 94],
	governmental : [53, 50, 12, 24, 17, 31, 85, 55, 46, 93, 91, 100],
	social : [1, 39, 48, 29, 66, 62, 92, 31, 5, 99, 28, 58 ]
}

var config = {
			type: 'line',
			data: {
				labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
				datasets: [{
					label: 'Social',
					backgroundColor: 'rgba(228, 103, 103, 0.5)',
					borderColor: 'rgba(228, 103, 103, 0.2)',
					data: dummy_data.social,
					fill: false,
				}, {
					label: 'Governmental',
					fill: false,
					backgroundColor: 'rgba(48, 137, 226, 0.5)',
					borderColor: 'rgba(48, 137, 226, 0.2)',
					data: dummy_data.governmental,
				}, {
					label: 'Environmental',
					fill: false,
					backgroundColor: 'rgba(52, 186, 119, 0.5)',
					borderColor: 'rgba(52, 186, 119, 0.2)',
					data: dummy_data.environmental,
				}]
			},
			options: {
				responsive: true,
				title: {
					display: true,
					text: 'Your ESG'
				},
				tooltips: {
					mode: 'nearest',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					xAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Month'
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Score'
						}
					}]
				},
				easing: 'linear'
			}
		};