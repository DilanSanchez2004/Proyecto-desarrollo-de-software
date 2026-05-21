document.addEventListener('DOMContentLoaded', () => {

    const cartItemCount   = document.querySelector('.cart-icon span');
    const cartItemsList   = document.querySelector('.cart-items');
    const cartTotal       = document.querySelector('.cart-total');
    const cartIcon        = document.querySelector('.cart-icon');
    const sidebar         = document.getElementById('sidebar');
    const sidebarClose    = document.querySelector('.sidebar-close');
    const checkoutBtn     = document.querySelector('.checkout-btn');

    // ── Persistencia ────────────────────────────────────────────────────────
    let cartItems   = JSON.parse(localStorage.getItem('cartItems'))   || [];
    let totalAmount = parseFloat(localStorage.getItem('totalAmount')) || 0;

    function saveCart() {
        localStorage.setItem('cartItems',   JSON.stringify(cartItems));
        localStorage.setItem('totalAmount', totalAmount.toFixed(3));
    }

    // ── Abrir / Cerrar sidebar ───────────────────────────────────────────────
    cartIcon.addEventListener('click',    () => sidebar.classList.add('open'));
    sidebarClose.addEventListener('click', () => sidebar.classList.remove('open'));

    // ── Agregar producto ─────────────────────────────────────────────────────
    // Los datos vienen de los atributos data-* del HTML dinámico (Jinja2)
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', () => {
            const card  = button.closest('.card');
            const id    = parseInt(card.dataset.id);
            const name  = card.dataset.nombre;
            const price = parseFloat(card.dataset.precio);

            const existing = cartItems.find(i => i.id === id);
            if (existing) {
                existing.quantity++;
            } else {
                cartItems.push({ id, name, price, quantity: 1 });
            }

            totalAmount += price;
            saveCart();
            updateCartUI();
            animateCartIcon();
        });
    });

    // ── Cambiar cantidad ─────────────────────────────────────────────────────
    function changeQuantity(id, delta) {
        const item = cartItems.find(i => i.id === id);
        if (!item) return;

        item.quantity += delta;
        totalAmount   += item.price * delta;

        if (item.quantity <= 0) {
            removeItem(id, false);
            return;
        }

        saveCart();
        updateCartUI();
    }

    // ── Eliminar producto ────────────────────────────────────────────────────
    function removeItem(id, recalculate = true) {
        const item = cartItems.find(i => i.id === id);
        if (!item) return;

        if (recalculate) totalAmount -= item.price * item.quantity;
        if (totalAmount < 0) totalAmount = 0;

        cartItems = cartItems.filter(i => i.id !== id);
        saveCart();
        updateCartUI();
    }

    // ── Actualizar UI ────────────────────────────────────────────────────────
    function updateCartUI() {
        updateCartItemCount();
        updateCartItemList();
        updateCartTotal();
    }

    function updateCartItemCount() {
        const total = cartItems.reduce((sum, i) => sum + i.quantity, 0);
        cartItemCount.textContent = total;
    }

    function updateCartItemList() {
        cartItemsList.innerHTML = '';

        if (cartItems.length === 0) {
            cartItemsList.innerHTML = '<p class="empty-cart">Tu carrito está vacío 🛒</p>';
            return;
        }

        cartItems.forEach(item => {
            const div = document.createElement('div');
            div.classList.add('cart-item');
            div.innerHTML = `
                <div class="individual-cart-item">
                    <span class="item-name">${item.name}</span>
                    <div class="item-controls">
                        <button class="qty-btn minus" data-id="${item.id}">−</button>
                        <span class="item-qty">${item.quantity}</span>
                        <button class="qty-btn plus"  data-id="${item.id}">+</button>
                    </div>
                    <span class="cart-item-price">
                        $${(item.price * item.quantity).toLocaleString('es-CO')}
                    </span>
                    <button class="remove-btn" data-id="${item.id}" title="Eliminar">✕</button>
                </div>
            `;
            cartItemsList.appendChild(div);
        });

        cartItemsList.querySelectorAll('.qty-btn.minus').forEach(btn =>
            btn.addEventListener('click', () => changeQuantity(parseInt(btn.dataset.id), -1))
        );
        cartItemsList.querySelectorAll('.qty-btn.plus').forEach(btn =>
            btn.addEventListener('click', () => changeQuantity(parseInt(btn.dataset.id), +1))
        );
        cartItemsList.querySelectorAll('.remove-btn').forEach(btn =>
            btn.addEventListener('click', () => removeItem(parseInt(btn.dataset.id)))
        );
    }

    function updateCartTotal() {
        cartTotal.textContent = `$${totalAmount.toLocaleString('es-CO')}`;
    }

    // ── Animación del ícono ──────────────────────────────────────────────────
    function animateCartIcon() {
        cartItemCount.classList.add('bump');
        cartItemCount.addEventListener('animationend',
            () => cartItemCount.classList.remove('bump'), { once: true }
        );
    }

    // ── Checkout → Flask ─────────────────────────────────────────────────────
    checkoutBtn.addEventListener('click', async () => {
        if (cartItems.length === 0) {
            alert('El carrito está vacío');
            return;
        }

        const payload = {
            id_mesa:         SESION.id_mesa,
            id_cliente_mesa: SESION.id_cliente_mesa,
            tipo_pedido:     SESION.tipo_pedido,
            items: cartItems.map(item => ({
                id_producto:     item.id,
                cantidad:        item.quantity,
                precio_unitario: item.price
            }))
        };

        checkoutBtn.disabled    = true;
        checkoutBtn.textContent = 'Enviando...';

        try {
            const res = await fetch('/pedido', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify(payload)
            });

            const data = await res.json();

            if (res.ok) {
                alert(`✅ Pedido #${data.id_pedido} recibido. ¡Gracias!`);
                cartItems   = [];
                totalAmount = 0;
                saveCart();
                updateCartUI();
                sidebar.classList.remove('open');
            } else {
                alert(`❌ Error: ${data.error}`);
            }

        } catch (err) {
            alert('No se pudo conectar con el servidor. Intenta de nuevo.');
            console.error(err);
        } finally {
            checkoutBtn.disabled    = false;
            checkoutBtn.textContent = 'Ordenar';
        }
    });

    // ── Carga inicial ────────────────────────────────────────────────────────
    updateCartUI();
});