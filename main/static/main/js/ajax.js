
document.addEventListener("DOMContentLoaded", () => {
    const categorySelect = document.getElementById("categoryFilter");
    if (categorySelect) {
        categorySelect.addEventListener("change", () => {
            const category = categorySelect.value;
            fetch(`/api/recipes/?category=${category}`)
                .then(res => res.json())
                .then(data => {
                    const recipeList = document.getElementById("recipeResults");
                    recipeList.innerHTML = "";
                    data.forEach(recipe => {
                        const div = document.createElement("div");
                        div.innerHTML = `
                            <h3>${recipe.name}</h3>
                            <p>Email: ${recipe.email}</p>
                            <p>Ingredients: ${recipe.ingredients}</p>
                            <p>Duration: ${recipe.duration}</p>
                            <p>Category: ${recipe.category}</p>
                            ${recipe.uploaded_file ? `<img src="/media/${recipe.uploaded_file}" width="200">` : ""}
                        `;
                        recipeList.appendChild(div);
                    });
                })
                .catch(err => console.error("Fetch error:", err));
        });
    }

    const ajaxForm = document.getElementById("ajaxRecipeForm");
    if (ajaxForm) {
        ajaxForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(ajaxForm);
            fetch("/api/submit-recipe/", {
                method: "POST",
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                const msg = document.getElementById("formMessage");
                if (data.success) {
                    msg.innerHTML = `<p style="color:green">${data.message}</p>`;
                    ajaxForm.reset();
                } else {
                    msg.innerHTML = `<p style="color:red">${JSON.stringify(data.errors)}</p>`;
                }
            })
            .catch(err => console.error("Submit error:", err));
        });
    }
});
