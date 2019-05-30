$(function () {
    $(document).on('click', '.btn-add', function (e) {
        e.preventDefault();
        if ($(".entry").length == $(this).parent().prev().data("max-entries")) return false;
        var controlForm = $('form:first'),
            currentEntry = $(this).parents('.entry:first'),
            newEntry = currentEntry.after($(currentEntry.clone()));
        newEntry.find('input').val('');
        controlForm.find('.entry:not(:last) .btn-add')
            .removeClass('btn-add').addClass('btn-remove')
            .html('<i data-feather="minus" />');
        feather.replace();
    }).on('click', '.btn-remove', function (e) {
        $(this).parents('.entry:first').remove();
        e.preventDefault();
        return false;
    });
});
