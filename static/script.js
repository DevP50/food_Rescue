setTimeout(() => {
            const alerts = document.querySelectorAll('.flash-message');
            alerts.forEach(alert => alert.style.display = 'none');
        }, 3000);

function ToggleFields() {
    var Role = document.getElementById("Role").value;
    var fields = document.getElementById("restaurantFields");

    if(Role == "Restaurant"){
      fields.style.display = "block";
    }else{
      fields.style.display = "None";
    }
}
window.onload = function (){
    if(this.navigator.geolocation) {
navigator.geolocation.getCurrentPosition (

        function  (position) {
            const lat = position.coords.Latitude;
            const lng = position.coords.Longitude;
           
            document.getElementById("Latitude").value = lat;
            document.getElementById("Longitude").value = lng;
                 
                 console.log("Latitude: ",lat);
                 console.log("Longitude: ",lng);
        },
        function (error) {
            console.log("Error getting location:",error.message);
        } 
);
}else{
    console.log("Geolocation")
}



}