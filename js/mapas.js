var mapa_santander = Vue.component('mapa-santander',{
    props: ["id","texto", "votos-si", "votos-no"],
    template: '#mapa-santander-template'
})

var mapa_colombia = Vue.component('mapa-colombia',{
    props: ["id","texto", "votos-si", "votos-no"],
    template: '#mapa-colombia-template'
})