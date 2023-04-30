/*
-------------------------------------------------------------------------- 
Função para obter a lista existente do servidor via requisição GET
--------------------------------------------------------------------------
*/
const getList = async () => {
    let url = 'http://127.0.0.1:5000/compras';
    fetch(url, {
        method: 'get',
    })
    .then((responde) => responde.json())
    .then((data) => {
        data.compras.forEach(item => insertList(item.descricao, item.valor, item.data))
    })
    .catch((error) => {
        console.error('Error:', error);
    });
        
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/

getList()



/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/

const postItem = async (inputDescricao, inputValor, inputData) => {
    const formData = new FormData();
    formData.append('descricao', inputDescricao);
    formData.append('valor', inputValor);
    formData.append('data', inputData);

    let url = 'http://127.0.0.1:5000/compra';
    fetch(url, {
        method: 'post',
        body: formData
    })
      .then((responde) => responde.json())
      .catch((error) => {
        console.error('Error:', error);
    });
}



/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/

const insertButton = (parent) => {
    let span = document.createElement("span");
    let txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/

const removeElement = () => {
  let close = document.getElementsByClassName("close");
  //var table = document.getElementById('mytable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const descricaoItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(descricaoItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/compra?descricao=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}
/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com descrição, valor e data
  --------------------------------------------------------------------------------------
*/

const novaCompra = () => {
    let inputDescricao = document.getElementById("novaDescricao").value;
    let inputValor = document.getElementById("novoValor").value;
    let inputData = document.getElementById("novaData").value;
  
    if (inputDescricao === '') {
      alert("Escreva a descricao de uma compra!");
    } else if (isNaN(inputValor)) {
      alert("Valor precisa ser números!");
    } else {
      insertList(inputDescricao, inputValor, inputData)
      postItem(inputDescricao, inputValor, inputData)
      alert("Compra adicionada!")
    }
  }

  
  /*
    --------------------------------------------------------------------------------------
    Função para inserir items na lista apresentada
    --------------------------------------------------------------------------------------
  */
  const insertList = (descricao, valor, data) => {
    var item = [descricao, valor, data]
    var table = document.getElementById('tabelaCompra');
    var row = table.insertRow();
  
    for (var i = 0; i < item.length; i++) {
      var cel = row.insertCell(i);
      cel.textContent = item[i];
    }
    insertButton(row.insertCell(-1))
    document.getElementById("novaDescricao").value = "";
    document.getElementById("novoValor").value = "";
    document.getElementById("novaData").value = "";
  
    removeElement()
  }
