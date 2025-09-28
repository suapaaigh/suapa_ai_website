// Setup new project page js
$(function () {
    $('.next').on('click', function () {

        var nextId = $(this).parents('.tab-pane').next().attr("id");
        $('a[href=\\#' + nextId + ']').tab('show');
        return false;
    })

    $('a[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
        //update progress
        var step = $(e.target).data('bs-step');
        var percent = (parseInt(step) / 4) * 100;

        $('.offcanvas .progress-bar').css({ width: percent + '%' });
        //$('.progress-bar').text("Step " + step + " of 5");
        //e.relatedTarget // previous tab
    })
});