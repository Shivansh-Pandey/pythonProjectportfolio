
function filterCategory(category) {
    const items = document.querySelectorAll('.item');
    items.forEach(item => {
        if (category === "All" || item.dataset.category === category) {
            item.style.display = "block";
        } else {
            item.style.display = "none";
        }
    });
}
