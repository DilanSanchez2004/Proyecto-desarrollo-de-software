document.addEventListener('DOMContentLoaded', () => {

    const addToCartButton = document.querySelectorAll('.add-to-cart');
    const cartItemCount = document.querySelector('.cart-icon span');
    const cartItemsList = document.querySelector('.cart-items');
    const cartTotal = document.querySelector('.cart-total');
    const cartIcon = document.querySelector('.cart-icon');
    const sidebar = document.getElementById('sidebar');
    const sidebarClose = document.querySelector('.sidebar-close');

    let cartItems = [];
    let totalAmount = 0;

    // Abrir carrito
    cartIcon.addEventListener('click', () => {
        sidebar.classList.add('open');
    });

    // Cerrar carrito
    sidebarClose.addEventListener('click', () => {
        sidebar.classList.remove('open');
    });

    // Agregar productos
    addToCartButton.forEach((button, index) => {

        button.addEventListener('click', () => {

            const item = {
                name: document.querySelectorAll('.card--title')[index].textContent,
                price: parseFloat(
                    document.querySelectorAll('.price')[index].textContent
                ),
                quantity: 1
            };

            const existingItem = cartItems.find(
                cartItem => cartItem.name === item.name
            );

            if (existingItem) {
                existingItem.quantity++;
            } else {
                cartItems.push(item);
            }

            totalAmount += item.price;

            updateCartUI();
        });

    });

    function updateCartUI() {
        updateCartItemCount();
        updateCartItemList();
        updateCartTotal();
    }

    function updateCartItemCount() {

        let totalQuantity = 0;

        cartItems.forEach(item => {
            totalQuantity += item.quantity;
        });

        cartItemCount.textContent = totalQuantity;
    }

    function updateCartItemList() {

        cartItemsList.innerHTML = '';

        cartItems.forEach(item => {

            const cartItem = document.createElement('div');

            cartItem.classList.add('cart-item');

            cartItem.innerHTML = `
                <span>(${item.quantity}x) ${item.name}</span>
                <span class="cart-item-price">
                    $${(item.price * item.quantity).toFixed(3)}
                </span>
            `;

            cartItemsList.appendChild(cartItem);
        });
    }

    function updateCartTotal() {
        cartTotal.textContent = `$${totalAmount.toFixed(3)}`;
    }

});