document.addEventListener('DOMContentLoaded', () => {
        let editPostButtons = document.querySelectorAll('.edit-post-button');
        let editPostForm = document.querySelector('#edit-post-form');
        let postPk;
        let content;
        let target;

        editPostButtons.forEach(button => {
            button.onclick = (event) => {
                target = event.target;
                postPk = target.dataset.postPk;

                fetch(`/post-content/${postPk}`)
                    .then(response => response.json())
                    .then(post => {
                        document.querySelector('#edit-post-content').innerHTML = post.content;
                        document.querySelector('#edit-post-pk').value = postPk;
                    });
            };
        });

        document.querySelector('#edit-post-content').onchange = (event) => {
            content = event.target.value
        }

        editPostForm.onsubmit = () => {
            fetch(`/edit-post/${postPk}`, {
                method: 'POST',
                body: JSON.stringify({
                    content: content,
                })
            })
                .then(response => response.json())
                .then(result => {
                    let post = target.parentNode.querySelector('.post-content')

                    if (result.message !== 'Post edited successfully.') {
                        let error = document.createElement('div');
                        error.innerHTML = `
                                    <div class="my-2 alert alert-danger alert-dismissible fade show" role="alert">
                                        ${result.message}
                                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                    </div>
                                `
                        post.appendChild(error);
                    } else {
                        post.innerHTML = content;

                        let editedBadge = document.createTextNode(' (edited)');
                        target.parentNode.querySelector('.post-timestamp').appendChild(editedBadge);

                        let success = document.createElement('div');
                        success.innerHTML = `
                                    <div class="my-2 alert alert-success alert-dismissible fade show" role="alert">
                                        ${result.message}
                                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                    </div>
                                `
                        post.appendChild(success);
                    }
                });

            return false;
        };
    }
);