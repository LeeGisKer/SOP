function ValidarUsuario() {
    var usuario = document.getElementById("usuario").value;
    var contraseña = document.getElementById("contraseña").value;
  
    if (usuario === "" || contraseña === "") {
      alert("Por favor, complete todos los campos.");
      return false; 
    }
  
    return true;
  }
