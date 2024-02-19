document.addEventListener('DOMContentLoaded', () => {
        let likePostButtons = document.querySelectorAll('.like-post-button');

        likePostButtons.forEach(button => {
                button.onclick = (event) => {
                    fetch(`/like-post/${event.target.dataset.postPk}`, {
                            method: 'POST',
                        }
                    )
                        .then(response => response.json())
                        .then(result => {
                                event.target.parentNode.querySelector('.like-count').innerHTML = result.likes;
                            }
                        );
                };
            }
        );
    }
);