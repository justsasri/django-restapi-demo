import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js';
import OverlayScrollbars from 'overlayscrollbars';

// import './images';
// // import Masonry from 'masonry-layout';
import './scss/main.scss';


document.addEventListener("DOMContentLoaded", function () {
    
  // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

  // BOOTSTRAP TOOLTIP
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  });

  // BOOTSTRAP POPOVER
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  popoverTriggerList.map(function (popoverTriggerEl) {
    let opts = {
      animation: true,
    }
    if (popoverTriggerEl.hasAttribute('data-bs-content-id')) {
      var content_id = popoverTriggerEl.getAttribute('data-bs-content-id')
      var content_el = document.getElementById(content_id)
      if (content_el != null) {
        opts.content = content_el.innerHTML;
      } else {
        opts.content = `content element with #${content_id} not found!`;
      }
      opts.html = true;
    }
    return new bootstrap.Popover(popoverTriggerEl, opts)
  })

//   var OverlayScrollbarsList = [].slice.call(document.querySelectorAll('.scrollbars'))
//   OverlayScrollbarsList.map(function (scrollbarsEl) {
//     return new OverlayScrollbars(scrollbarsEl, {});
//   })

});


window.bootstrap = bootstrap;
// window.OverlayScrollbars = OverlayScrollbars;
