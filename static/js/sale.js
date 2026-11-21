/**
 * Sale form – dynamic add/remove rows and auto-calculate totals.
 * Works with Django's inline formset management form.
 */
document.addEventListener('DOMContentLoaded', function () {
    const formsetBody = document.getElementById('formsetBody');
    const addRowBtn = document.getElementById('addRow');
    const grandTotalEl = document.getElementById('grandTotal');

    if (!formsetBody || !addRowBtn) return;

    const prefix = 'items';  // Django formset prefix

    function getTotalFormsInput() {
        return document.getElementById(`id_${prefix}-TOTAL_FORMS`);
    }

    // ── Add Row ──────────────────────────────────────────────────
    addRowBtn.addEventListener('click', function () {
        const totalForms = getTotalFormsInput();
        const formNum = parseInt(totalForms.value);

        // Clone the first row and clear values
        const firstRow = formsetBody.querySelector('.sale-item-row');
        if (!firstRow) return;

        const newRow = firstRow.cloneNode(true);

        // Update IDs and names
        newRow.querySelectorAll('select, input').forEach(input => {
            if (input.name) {
                input.name = input.name.replace(/-\d+-/, `-${formNum}-`);
            }
            if (input.id) {
                input.id = input.id.replace(/-\d+-/, `-${formNum}-`);
            }
            // Reset values
            if (input.type === 'checkbox') {
                input.checked = false;
            } else if (input.tagName === 'SELECT') {
                input.selectedIndex = 0;
            } else if (input.type !== 'hidden') {
                input.value = '';
            } else {
                input.value = '';
            }
        });

        // Clear error messages
        newRow.querySelectorAll('.text-danger').forEach(el => el.remove());

        // Reset subtotal
        const subtotalCell = newRow.querySelector('.subtotal-cell');
        if (subtotalCell) subtotalCell.textContent = '₹0.00';

        formsetBody.appendChild(newRow);
        totalForms.value = formNum + 1;

        attachRowListeners(newRow);
    });

    // ── Remove Row ───────────────────────────────────────────────
    formsetBody.addEventListener('click', function (e) {
        const btn = e.target.closest('.remove-row');
        if (!btn) return;

        const rows = formsetBody.querySelectorAll('.sale-item-row');
        if (rows.length <= 1) {
            alert('At least one item is required.');
            return;
        }

        const row = btn.closest('.sale-item-row');
        // Check if this row has a DELETE checkbox (existing saved items)
        const deleteCheckbox = row.querySelector('input[type="checkbox"][name*="DELETE"]');
        if (deleteCheckbox) {
            deleteCheckbox.checked = true;
            row.style.display = 'none';
        } else {
            row.remove();
            // Update TOTAL_FORMS
            const totalForms = getTotalFormsInput();
            totalForms.value = parseInt(totalForms.value) - 1;
            reindexRows();
        }
        updateGrandTotal();
    });

    // ── Auto-calculate subtotals ─────────────────────────────────
    function attachRowListeners(row) {
        const qtyInput = row.querySelector('input[name*="quantity"]');
        const priceInput = row.querySelector('input[name*="unit_price"]');

        if (qtyInput) qtyInput.addEventListener('input', () => updateSubtotal(row));
        if (priceInput) priceInput.addEventListener('input', () => updateSubtotal(row));
    }

    function updateSubtotal(row) {
        const qty = parseFloat(row.querySelector('input[name*="quantity"]')?.value) || 0;
        const price = parseFloat(row.querySelector('input[name*="unit_price"]')?.value) || 0;
        const subtotal = qty * price;
        const subtotalCell = row.querySelector('.subtotal-cell');
        if (subtotalCell) {
            subtotalCell.textContent = '₹' + subtotal.toFixed(2);
        }
        updateGrandTotal();
    }

    function updateGrandTotal() {
        let total = 0;
        formsetBody.querySelectorAll('.sale-item-row').forEach(row => {
            if (row.style.display === 'none') return; // skip deleted
            const qty = parseFloat(row.querySelector('input[name*="quantity"]')?.value) || 0;
            const price = parseFloat(row.querySelector('input[name*="unit_price"]')?.value) || 0;
            total += qty * price;
        });
        if (grandTotalEl) {
            grandTotalEl.textContent = '₹' + total.toFixed(2);
        }
    }

    function reindexRows() {
        const rows = formsetBody.querySelectorAll('.sale-item-row');
        rows.forEach((row, idx) => {
            row.querySelectorAll('select, input').forEach(input => {
                if (input.name) {
                    input.name = input.name.replace(/-\d+-/, `-${idx}-`);
                }
                if (input.id) {
                    input.id = input.id.replace(/-\d+-/, `-${idx}-`);
                }
            });
        });
    }

    // Attach listeners to existing rows
    formsetBody.querySelectorAll('.sale-item-row').forEach(row => {
        attachRowListeners(row);
        updateSubtotal(row);
    });
});
