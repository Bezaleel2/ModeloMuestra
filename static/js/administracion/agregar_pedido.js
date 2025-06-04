document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('item-forms-container');
    const addButton = document.getElementById('add-item-button');
    const totalFormsInput = document.querySelector('input[name$="-TOTAL_FORMS"]'); // Busca input cuyo nombre TERMINA con -TOTAL_FORMS
    const emptyFormTemplateDiv = document.getElementById('empty-form-template');

    // Validaciones para asegurar que los elementos existen antes de continuar
    if (!totalFormsInput) {
        console.error("El campo de gestión del formset 'TOTAL_FORMS' no se encontró.");
        if (addButton) addButton.style.display = 'none'; // Ocultar botón si no puede funcionar
        return; // Detener ejecución si falta este campo crucial
    }

    if (!emptyFormTemplateDiv || !emptyFormTemplateDiv.firstElementChild) {
        console.error("La plantilla para el nuevo ítem del formset (empty-form-template) no se encontró o está vacía.");
        if (addButton) addButton.style.display = 'none';
        return;
    }
    
    // Clonamos el nodo .item-form-row que está dentro del div#empty-form-template
    const emptyFormRowNode = emptyFormTemplateDiv.firstElementChild.cloneNode(true);
    
    // Obtenemos el prefijo del formset del nombre del input TOTAL_FORMS
    // ej. si es "items-TOTAL_FORMS", el prefijo es "items"
    const formsetPrefix = totalFormsInput.name.split('-')[0];

    if (addButton && container) { // Asegurarse que el botón y el contenedor principal existen
        addButton.addEventListener('click', function() {
            let newFormIdx = parseInt(totalFormsInput.value); // El índice para el nuevo formulario

            // Clonamos la estructura de la fila del formulario vacío
            let newRow = emptyFormRowNode.cloneNode(true);
            
            // Actualizamos el HTML interno del clon reemplazando '__prefix__' por el nuevo índice
            // Esto actualiza los atributos 'name', 'id', etc., de los campos del formulario.
            let newRowHtml = newRow.innerHTML.replace(/__prefix__/g, newFormIdx);
            newRow.innerHTML = newRowHtml; // Reasignamos el HTML modificado al clon

            // Opcional: Limpiar valores de los inputs si el empty_form no viene completamente vacío
            // o si se clonó una fila con datos residuales (aunque empty_form debería estar limpio).
            newRow.querySelectorAll('input[type="text"], input[type="number"], select').forEach(input => {
                if (input.type !== 'hidden' && !input.name.includes('DELETE')) {
                    // Para select, podrías querer resetear al primer option (el vacío)
                    if (input.tagName === 'SELECT') {
                        input.selectedIndex = 0; 
                    } else {
                        input.value = ''; // Limpiar otros inputs
                    }
                }
            });
            // Asegurar que los checkboxes de DELETE (si existieran en el empty_form) no estén marcados
            newRow.querySelectorAll('input[type="checkbox"][name*="DELETE"]').forEach(cb => cb.checked = false);


            container.appendChild(newRow); // Añadimos la nueva fila al contenedor
            totalFormsInput.value = newFormIdx + 1; // Incrementamos el contador TOTAL_FORMS
        });
    } else {
        // Si el botón o el contenedor de ítems no se encuentran, advertimos y ocultamos el botón
        if (addButton) addButton.style.display = 'none';
        console.warn("El botón para agregar ítems o el contenedor de ítems no se encontró. La funcionalidad de agregar dinámicamente no estará disponible.");
    }
});