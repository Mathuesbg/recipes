function my_scope() {
    const forms = document.querySelectorAll('.form-delete');
    
    for (const form of forms) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const confirmation = confirm("Are you sure you want to delete this item?");
            if (confirmation) {
                form.submit();
            }
        });
    }
}

my_scope();