let user_id = localStorage.getItem("user_id");

// ---------------- REGISTER ----------------
function register() {
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    fetch("http://localhost:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
    })
    .catch(err => alert("Server error"));
}

// ---------------- LOGIN ----------------
function login() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {

        if (data.success) {
            localStorage.setItem("user_id", data.user_id);
            alert("Login successful");
            window.location = "menu.html";
        } else {
            alert("Invalid credentials");
        }

    })
    .catch(err => alert("Server error"));
}

// ---------------- LOAD PRODUCTS ----------------
function loadProducts() {
    fetch("http://localhost:5000/products")
    .then(res => res.json())
    .then(data => {
        window.allProducts = data;
        displayProducts(data);
    });
}

// ---------------- DISPLAY PRODUCTS ----------------
function displayProducts(data) {
    let html = "";

    data.forEach(p => {
        html += `
        <div class="card">
            <img src="https://source.unsplash.com/300x200/?food" />
            <div class="card-body">
                <h3>${p.name}</h3>
                <p>${p.description || "Delicious food"}</p>
                <p class="price">₹${p.price}</p>
                <button onclick="addToCart(${p.id})">Add to Cart</button>
            </div>
        </div>`;
    });

    document.getElementById("menu").innerHTML = html;
}

// ---------------- ADD TO CART ----------------
function addToCart(id) {

    if (!user_id) {
        alert("Please login first");
        return;
    }

    fetch("http://localhost:5000/add_to_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, product_id: id })
    })
    .then(res => res.json())
    .then(data => alert(data.message))
    .catch(err => alert("Server error"));
}

// ---------------- LOAD CART ----------------
function loadCart() {

    fetch(`http://localhost:5000/cart/${user_id}`)
    .then(res => res.json())
    .then(data => {

        let html = "";
        let total = 0;

        data.forEach(c => {
            total += c.price;
            html += `<p>${c.name} - ₹${c.price}</p>`;
        });

        document.getElementById("cart").innerHTML = html;
        document.getElementById("total").innerText = "Total: ₹" + total;
    });
}

// ---------------- PLACE ORDER ----------------
function placeOrder() {

    if (!user_id) {
        alert("Login required");
        return;
    }

    fetch(`http://localhost:5000/order/${user_id}`, {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        loadCart();
    })
    .catch(err => alert("Server error"));
}

// ---------------- ORDER HISTORY ----------------
function loadOrderHistory() {

    fetch(`http://localhost:5000/orders/${user_id}`)
    .then(res => res.json())
    .then(data => {

        let html = "";

        data.forEach(o => {
            html += `<p>Order #${o.id} - ₹${o.total}</p>`;
        });

        document.getElementById("orders").innerHTML = html;
    });
}

// ---------------- ADMIN ORDERS ----------------
function loadOrders() {

    fetch("http://localhost:5000/admin/orders")
    .then(res => res.json())
    .then(data => {

        let html = "";

        data.forEach(o => {
            html += `<p>Order #${o.id} - ₹${o.total}</p>`;
        });

        document.getElementById("orders").innerHTML = html;
    });
}