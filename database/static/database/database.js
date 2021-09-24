document.addEventListener('DOMContentLoaded', function() {

    // Load all the songs
    load_contents()

    // Handle keypress input on the search bar. Should only show ones that match the input
    document.querySelector("#search").addEventListener('keyup', event => {
        searchTerm = document.querySelector('#search').value

        // i means ignore case
        let re = new RegExp(searchTerm, 'i')

        // Find all the ones that DON"T match (returns -1)
        const filtered_list = song_list.filter(song => {

        //Get the song-list DOM element
        const songlist = document.querySelector('#song-list')

            // Choose whether to display
            display = song.title.search(re) >= 0
            if (display){
                songlist.querySelector(`#id-${song.id}`).style.display = "block"
            }
            else
            songlist.querySelector(`#id-${song.id}`).style.display = "none"
            return display
        })
    })

})

song_list = ""

// Fetch all the songs
function load_contents() {

    // Send the Json request containing post_id, and content
    fetch('/fetch_songs', {
    method: 'GET',
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result)
        song_list = result.song_list

    });
}

// Send JSON request to remove song from book
function remove_song_to_book(id){
    const book_id = JSON.parse(document.getElementById('book_id').textContent);
    fetch('/song_to_book', {
        method: 'POST',
        body: JSON.stringify({
            song_id: id,
            book_id: book_id,
            method:"remove"
        })
    })
    .then(response => response.json())
    .then(result => {
        // Remove the song from the book list
        child = document.querySelector('#book-song-list').querySelector(`#id-${result.song.id}`)
        document.querySelector('#book-song-list').removeChild(child)
        
        // Make the song selectable in the list
        document.querySelector('#song-list').querySelector(`#id-${result.song.id}`).classList.remove("selected")
    })
}

// Send JSON request to add song to book
function add_song_to_book(id){
    const book_id = JSON.parse(document.getElementById('book_id').textContent);

    fetch('/song_to_book', {
        method: 'POST',
        body: JSON.stringify({
            song_id: id,
            book_id: book_id,
            method:"add"
        })
    })
    .then(response => response.json())
    .then(result => {
        // Return a new HTML element in the Book List
        document.querySelector('#book-song-list').append(createSongBookElement(result.song))
        
        // Make the song unselectable in the list
        document.querySelector('#song-list').querySelector(`#id-${result.song.id}`).classList.add("selected")
    })
}

// Create a new HTML element for a song (in a book)
function createSongBookElement(song) {
    const e = document.createElement("div")
    e.classList = "book-item"
    e.id = `id-${song.id}`
    e.dataset.id = song.id
    e.innerHTML = song.title
    e.onclick = () => {remove_song_to_book(song.id) }
    return e
}

// Confirm deleting book
function confirmDeleteBook(event){
    if (confirm('Are you sure you want to delete this book forever?')) {
        return true
        } else {
        window.event.preventDefault()
        return false
    }
}


