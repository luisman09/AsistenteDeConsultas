




function alertaNoSelect() {
    alert("No seleccionaste ningún elemento para mostrar.");
}

//Esta no quiere funcionar
$('#first').click(function() {
    $.ajax({
        url: "{% url 'asistente_de_consultas:hello' %}",
        type: "get",
        success: function(data) {
            alert(data);
        },
        error: function(data) { 
            alert("Got an error dude");
        }
    });
});

