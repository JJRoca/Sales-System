document.addEventListener('DOMContentLoaded', () => {
  // get elements by their respective IDS
  const btnSearchProducts = document.getElementById('btnSearchProducts');
  const modalSearchProducts = document.getElementById('myModalSearchProducts');
  //GET elemtns of forms.py
  const id_subTotal = document.getElementById("id_subtotal");
  const iva=document.getElementById("id_iva");
  const ivaCalculate=document.getElementById("ivaCalculate");
  const total=document.getElementById("id_total")
  // Find the element with the class '.clasePadre' 
  const tableBody = document.querySelector('.clasePadre');
  const btnCloseModal = document.querySelector('.close');
  const searchInput = document.getElementById('searchInput');

  const tableValues = document.getElementById('values');       
  // Define an arrow function to create a table row
  const createRow = (item) => {
    // Create a table row element
    const row = document.createElement('tr'); 
    //  create tables cells for different properties of the 'item' 
    const nameCell = document.createElement("td");
    nameCell.className = 'product';
    nameCell.textContent = item.name;            
    // Create a table cell for the image
    const imageCell = document.createElement('td');
    const image = document.createElement('img');
    image.src = "/media/" + item.image; // Image path
    image.alt = ""; // add an "alt"atribute if needed
    image.style.width = "30px";
    image.style.height = "20px";
    imageCell.appendChild(image);
    const stockCell = document.createElement("td");
    stockCell.textContent = item.stock;
    const priceCell = document.createElement("td");
    priceCell.textContent = item.price;

    const optionCell = document.createElement("td");
    const icon=document.createElement("i");
    icon.className = "fas fa-plus"; // Clases de Font Awesome para el icono "add"
    optionCell.appendChild(icon);
    // Add each cell as a child to the row
    row.appendChild(nameCell);
    row.appendChild(imageCell);
    row.appendChild(stockCell);
    row.appendChild(priceCell);  
    row.appendChild(optionCell);
    
    // add a click event handler to the row
    icon.addEventListener('click', (e) => {
      let name = item.name;                
      fetch(`/get-product-details/?name=${name}`)
      .then((response) => response.json())
      .then(data=>{
        const r = document.createElement("tr");
        
        const id=document.createElement("input");
        id.setAttribute("name","id")
        id.value=data.id
        id.style.display="none"

        const dele = document.createElement("td");
        const icoDelete = document.createElement("i");
        icoDelete.className = "fas fa-trash"
        dele.appendChild(icoDelete);
                
        const name = document.createElement("td");
        name.textContent=data.name

        const stock = document.createElement("td");
        stock.textContent = data.stock;
        
        const price = document.createElement("td");
        price.textContent = data.price;

        const canP=document.createElement('td');
        const cantidad = document.createElement("input");
        cantidad.setAttribute("name","cantidad");
        cantidad.value = 1
  
        canP.appendChild(cantidad)
        const subTotal = document.createElement("td");
        subTotal.textContent = price.textContent
        //function to calculate subtotal of table with the id="tblProducts"
        const CalculateSubTotal = (cantidad,price,subTotal) => {
          let cantidadValue=parseInt(cantidad.value);
          if(isNaN(cantidadValue) || cantidadValue<=0){
            subTotal.textContent = (0).toFixed(2)
            }else{
              subTotal.textContent = (cantidadValue*parseFloat(price.textContent)).toFixed(2)
            }
          }
         //create an addEventListerner input to verify if the input field has changed
        cantidad.addEventListener("input",()=>{
            CalculateSubTotal(cantidad,price,subTotal);
            recalculateTotal();        
          })
        //function to calculate el {{form.subtotal}}ivaCalculate and {{forms.total}}  
        const recalculateTotal=()=>{
              // Selecciona la tabla por su ID
              const table = document.getElementById('tblProducts');
              // Obtiene todas las filas en la tabla
              const rows = table.querySelectorAll('tbody tr');
              let suma = 0;
              let lista = [];
              rows.forEach((row) => {
                  const cells = row.querySelectorAll('td');
                  const rowData = {
                      sub_total: parseFloat(cells[5].textContent),
                  };
                  // const rowData=parseFloat(cells[5].textContent)
                  lista.push(rowData);
              });
              
              for (let item of lista) {
                  suma += item.sub_total;
              }
              ivaCalculate.value=(suma*parseFloat(iva.value)).toFixed(2)
              id_subTotal.value = suma.toFixed(2); // Asegúrate de que el resultado tenga 2 decimales
              total.value=(parseFloat(ivaCalculate.value)+parseFloat(id_subTotal.value)).toFixed(2);
              // return id_subTotal;
        }
        //when the user clicks on delete icon, delete the table row
        icoDelete.addEventListener("click",()=>{
          r.remove();
          recalculateTotal();  
        })
        r.appendChild(id)
        r.appendChild(dele)
        r.appendChild(name);
        r.appendChild(stock);
        r.appendChild(price);
        r.appendChild(canP);
        r.appendChild(subTotal);
        tableValues.appendChild(r);
        recalculateTotal();  
        //Clear to table
        tableBody.innerHTML = "";
        modalSearchProducts.style.display = "none";
        })
        .catch(error => {
          console.log(error)
        })
      
        });
    return row; 
    }
   
  btnSearchProducts.addEventListener("click", ()=> {
      // Add the 'show' class to the 'modalSearchProducts' element
      modalSearchProducts.classList.add("show");

      // Set the 'display' style property to 'block' for 'modalSearchProducts'
      modalSearchProducts.style.display = "block";
      // if the value is null or empty, then the table will be cleared
      if(searchInput.value === ""){
        tableBody.innerHTML = "";
        return
      }
      // Perform a fetch request to '/search/' with a filter parameter from 'searchInput'
      fetch(`/search/?filter=${searchInput.value}`)
      .then(response=>response.json())
      .then(data=>{
        if (data.error){
          console.log(data.error)
          return;
        }
        //when fetch request is successful   
        //Iterate through each 'items' in data and create a row using the 'createRow' function
        data.forEach(items=>{
        const row=createRow(items);
        //Append the created row to the 'tableBody'
        tableBody.appendChild(row);
      })         
      })
      .catch(e=>{
        console.log(e)
      })
    });

    // event to close the modal
  btnCloseModal.addEventListener("click", ()=> {
      //Clear to the table
      tableBody.innerHTML = "";
      modalSearchProducts.style.display = "none";
    });
//When the user clicks on button submit the event submit 
  addEventListener("submit",(e)=>{
    const filas=tableValues.getElementsByTagName("tr")
    if(filas.length===0){
      e.preventDefault();
      bootbox.alert({
        message: 'You must have at least one product in your product detail table.',
        className: 'rubberBand animated'
        });
    }else{
      
    }
  })
});