// progressbar.js@1.0.0 version is used
// Docs: http://progressbarjs.readthedocs.org/en/1.0.0/

var bar = new ProgressBar.Circle(container1, {
  color: '#FFEA82',
  trailColor: '#eee',
  trailWidth: 1,
  duration: 1400,
  easing: 'bounce',
  strokeWidth: 6,
  from: {color: '#FFEA82', a:0},
  to: {color: '#ED6A5A', a:1},
  // Set default step function for all animate calls
  step: function(state, circle) {
    circle.path.setAttribute('stroke', state.color);
		

	 var value = Math.round(circle.value() * 200);
    if (value === 0) {
      circle.setText('');
    } else {
      circle.setText(value);
    }

  }
});

bar.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
bar.text.style.fontSize = '2rem';

bar.animate(1.0);  // Number from 0.0 to 1.0





var bar = new ProgressBar.Circle(container2, {
  color: '#FFEA82',
  trailColor: '#eee',
  trailWidth: 1,
  duration: 1400,
  easing: 'bounce',
  strokeWidth: 6,
  from: {color: '#FFEA82', a:0},
  to: {color: '#ED6A5A', a:1},
  // Set default step function for all animate calls
  step: function(state, circle) {
    circle.path.setAttribute('stroke', state.color);
		

	 var value = Math.round(circle.value() * 200);
    if (value === 0) {
      circle.setText('');
    } else {
      circle.setText(value);
    }

  }
});

bar.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
bar.text.style.fontSize = '2rem';

bar.animate(1.0);  // Number from 0.0 to 1.0



var bar = new ProgressBar.Circle(container3, {
  color: '#FFEA82',
  trailColor: '#eee',
  trailWidth: 1,
  duration: 1400,
  easing: 'bounce',
  strokeWidth: 6,
  from: {color: '#FFEA82', a:0},
  to: {color: '#ED6A5A', a:1},
  // Set default step function for all animate calls
  step: function(state, circle) {
    circle.path.setAttribute('stroke', state.color);
		

	 var value = Math.round(circle.value() * 200);
    if (value === 0) {
      circle.setText('');
    } else {
      circle.setText(value);
    }

  }
});

bar.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
bar.text.style.fontSize = '2rem';

bar.animate(1.0);  // Number from 0.0 to 1.0


var bar = new ProgressBar.Circle(container4, {
  color: '#FFEA82',
  trailColor: '#eee',
  trailWidth: 1,
  duration: 1400,
  easing: 'bounce',
  strokeWidth: 6,
  from: {color: '#FFEA82', a:0},
  to: {color: '#ED6A5A', a:1},
  // Set default step function for all animate calls
  step: function(state, circle) {
    circle.path.setAttribute('stroke', state.color);
		

	 var value = Math.round(circle.value() * 200);
    if (value === 0) {
      circle.setText('');
    } else {
      circle.setText(value);
    }

  }
});

bar.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
bar.text.style.fontSize = '2rem';

bar.animate(1.0);  // Number from 0.0 to 1.0