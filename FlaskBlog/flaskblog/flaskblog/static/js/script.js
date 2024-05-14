//  cancel flash messages from flask
function cancelFlashMessage() {
    document.addEventListener('DOMContentLoaded', function() {
        let cancelSuccessFlash = document.querySelector('.success-flash-btn');
        let cancelErrorFlash = document.querySelector('.error-flash-btn');
        let cancelInfoFlash = document.querySelector('.info-flash-btn');

        if (cancelSuccessFlash) {
            cancelSuccessFlash.addEventListener('click', function() {
                document.querySelector('.success-remove-bg').style.display = 'none';
            });
        }

        if (cancelErrorFlash) {
            cancelErrorFlash.addEventListener('click', function() {
                document.querySelector('.error-remove-bg').style.display = 'none';
            });
        }

        if (cancelInfoFlash) {
            cancelInfoFlash.addEventListener('click', function() {
                document.querySelector('.info-remove-bg').style.display = 'none';
            });
        }
    });
}

//  Delete post logic
function deletePost() {
    let revelDeleteModal = document.querySelectorAll('.delete-btn')
    if (revelDeleteModal) {
        revelDeleteModal.forEach(element => {
            element.addEventListener('click', function(){
                document.querySelector('.none').style.display = 'flex'
                document.body.style.backgroundColor = '#00000066';

                // dynamically construct url for delete view function in the form action
                let postId = element.getAttribute('data-post-id');
                let form = document.querySelector(".delete_form");
                form.action = `/delete/${postId}`;
            })
        })
    }
}


function cancelModal(){
    let cancelDeleteModal = document.querySelectorAll('.cancel-delete-modal')
    if (cancelDeleteModal){
        cancelDeleteModal.forEach(element => {
            element.addEventListener('click', function(){ 
                document.querySelector('.none').style.display = 'none'
                document.body.style.backgroundColor = ''
            })
        });
    }

}






// Function call
cancelFlashMessage();
deletePost();
cancelModal();

