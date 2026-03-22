setTimeout(() => {
            const alerts = document.querySelectorAll('.flash-message');
            alerts.forEach(alert => alert.style.display = 'none');
        }, 3000);