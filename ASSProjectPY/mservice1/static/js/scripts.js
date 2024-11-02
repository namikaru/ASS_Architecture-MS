document.getElementById('addBookForm').addEventListener('submit', function(event) {
    event.preventDefault();
   
    var data = {
        title: document.getElementById('title').value,
        author: document.getElementById('author').value,
    };

    fetch('/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })

    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);

        // Add the new book to the list
        var bookList = document.getElementById('book-list');
        var newBook = document.createElement('li');
        var bookCount = bookList.getElementsByTagName('li').length + 1;  // Count current items
        newBook.id = `book-${data.id}`;
        newBook.innerHTML = `<span style="font-weight: bold;">${bookCount}.</span> ${data.title} by ${data.author}
            <a href="/edit/${data.id}"><button type="button" class="button-name">Edit</button></a>
            <button class="delete-button" data-id="${data.id}">Delete</button>`;
        bookList.appendChild(newBook);

        // Reset input fields
        document.getElementById('title').value = '';
        document.getElementById('author').value = '';

        // Show notification
        var notification = document.getElementById('notification');
        notification.textContent = 'Book Added!';
        notification.className = 'added';
        notification.style.display = 'block';
        setTimeout(function() {
            notification.style.opacity = '0';
        }, 2000); // Display notification for 2 seconds
        setTimeout(function() {
            notification.style.display = 'none';
            notification.style.opacity = '1'; // Reset opacity for next time
        }, 3000); // Hide notification after 3 seconds
    })
   
    .catch((error) => {
        console.error('Error:', error);
    });
});

document.addEventListener('click', function(event) {
    if (event.target && event.target.className === 'delete-button') {
        var bookId = event.target.getAttribute('data-id');
        fetch('/delete/' + bookId, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
     
        .then(response => response.json())
        .then(data => {
            console.log('Deleted:', data);
            // Remove the book from the list
            var bookItem = document.getElementById('book-' + bookId);
            bookItem.remove();

            // Renumber the remaining books
            var bookList = document.getElementById('book-list');
            var listItems = bookList.getElementsByTagName('li');
            for (var i = 0; i < listItems.length; i++) {
                listItems[i].getElementsByTagName('span')[0].textContent = (i + 1) + '.';
            }

            // Show delete notification
            var notification = document.getElementById('notification');
            notification.textContent = 'Book Deleted!';
            notification.className = 'deleted';
            notification.style.display = 'block';
            setTimeout(function() {
                notification.style.opacity = '0';
            }, 2000); // Display notification for 2 seconds
            setTimeout(function() {
                notification.style.display = 'none';
                notification.style.opacity = '1'; // Reset opacity for next time
            }, 3000); // Hide notification after 3 seconds
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});
