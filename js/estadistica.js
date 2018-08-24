var comp_estadistica = Vue.component('estadistica',{
    props: ["hora", "potsuf", "porcmesas", "boletin"],
    template: '#estadisticas-template',
    methods: {
        formatPrice(value) {
            let val = value;
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        },
        formatTime(time){
            return moment(time,"H:mm").format("h:mm a");
        }
    }
})