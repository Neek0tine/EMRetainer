function readURL(input) {
    if (input.files && input.files[0]) {
        var reader  = new FileReader();

        reader.onload = function (e) {
            $('#blah')
                .attr('src', e.target.result)
                .width(579)
                .height(837);
        };

        reader.readAsDataURL(input.files[0]);
    }
}