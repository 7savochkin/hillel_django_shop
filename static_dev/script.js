function add_or_delete_favourites(element) {
    let productID = element.data('product'),
        heart = element.find('svg.bi-heart'),
        heartFill = element.find('svg.bi-heart-fill');
    $.get(`/ajax-add-or-delete-to-favourites/${productID}`, function (data) {
        if (data.attached === true) {
            heart.addClass('d-none')
            heartFill.removeClass('d-none')
        } else {
            heartFill.addClass('d-none')
            heart.removeClass('d-none')
        }
    }).fail(function (error) {
        console.log(error);
    });
}