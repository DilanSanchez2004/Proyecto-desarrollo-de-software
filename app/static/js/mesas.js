document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('qrModal');
    const modalTitle = document.getElementById('modalTitle');
    const qrContainer = document.getElementById('qrCodeContainer');
    const printBtn = document.getElementById('printQrBtn');
    let currentQrCode = null;
    let currentMesaNum = '';

    // Cerrar modal (todos los botones con clase .modal-close)
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', () => {
            modal.style.display = 'none';
            if (qrContainer) qrContainer.innerHTML = '';
            currentQrCode = null;
        });
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
            if (qrContainer) qrContainer.innerHTML = '';
            currentQrCode = null;
        }
    });

    // Delegación de eventos para los botones de Ver QR
    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-ver-qr');
        if (!btn) return;

        const idMesa = btn.dataset.id;
        currentMesaNum = btn.dataset.numero;

        // Generar la URL absoluta de la mesa
        const protocol = window.location.protocol;
        const host = window.location.host;
        const url = `${protocol}//${host}/mesa/${idMesa}`;

        modalTitle.textContent = `Código QR - Mesa ${currentMesaNum}`;
        qrContainer.innerHTML = '';

        // Instanciar QRCode (qrcode.js)
        currentQrCode = new QRCode(qrContainer, {
            text: url,
            width: 256,
            height: 256,
            colorDark: "#1e293b", // Slate 800
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.H
        });

        // Mostrar modal
        modal.style.display = 'flex';
    });

    // Lógica para imprimir el QR
    if (printBtn) {
        printBtn.addEventListener('click', () => {
            if (!qrContainer) {
                alert('El código QR no se ha generado por completo.');
                return;
            }

            const canvas = qrContainer.querySelector('canvas');
            const img = qrContainer.querySelector('img');
            const imgSrc = canvas ? canvas.toDataURL('image/png') : (img ? img.src : null);

            if (!imgSrc) {
                alert('El código QR no se ha generado por completo.');
                return;
            }

            // Abrir una ventana nueva para imprimir el QR de manera limpia
            const printWindow = window.open('', '_blank', 'width=600,height=600');
            printWindow.document.write(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Imprimir QR Mesa ${currentMesaNum}</title>
                    <style>
                        body {
                            font-family: 'Inter', system-ui, -apple-system, sans-serif;
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            justify-content: center;
                            height: 100vh;
                            margin: 0;
                            text-align: center;
                            background-color: #ffffff;
                            color: #1e293b;
                        }
                        .qr-card {
                            border: 3px solid #1e293b;
                            border-radius: 16px;
                            padding: 30px;
                            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
                            max-width: 320px;
                        }
                        h1 {
                            margin-top: 0;
                            font-size: 28px;
                            font-weight: 800;
                            letter-spacing: -0.025em;
                        }
                        p {
                            font-size: 14px;
                            color: #64748b;
                            margin-top: 10px;
                            margin-bottom: 25px;
                        }
                        img {
                            width: 240px;
                            height: 240px;
                            display: block;
                            margin: 0 auto;
                        }
                        @media print {
                            body {
                                height: auto;
                            }
                            .qr-card {
                                border: none;
                                box-shadow: none;
                                padding: 0;
                            }
                        }
                    </style>
                </head>
                <body>
                    <div class="qr-card">
                        <h1>MESA ${currentMesaNum}</h1>
                        <p>Escanea este código QR para ver el menú y realizar tu pedido</p>
                        <img src="${imgSrc}" />
                    </div>
                    <script>
                        window.onload = function() {
                            window.print();
                            setTimeout(function() { window.close(); }, 500);
                        };
                    </script>
                </body>
                </html>
            `);
            printWindow.document.close();
        });
    }
});
