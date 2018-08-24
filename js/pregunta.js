var img_umbral = Vue.component('umbralimg',{
    props:["valor", "tipo", "validos"],
    computed:{
        imagen: function (){
            if (this.tipo == 'si'){
                let ruta_imagen = (this.valor > ( this.validos /2 ) +1 )? 'img/si_n.jpg' : 'img/si_s.jpg';
                return  ruta_imagen;
            }else{
                let ruta_imagen = (this.valor > ( this.validos /2 ) +1 )? 'img/no_n.jpg' : 'img/no_s.jpg';
                return  ruta_imagen;
            }
        }
    },
    template: '#img-umbral'
})

var comp_voto = Vue.component('votos',{
    props: ["valor", "tipo", "validos"],
    data: function(){
        if (this.tipo=='si'){
            return {
                estiloTexto:{
                    textAlign: 'right'
                }
            }
        }else{
            return {
                estiloTexto:{
                    textAlign:'left'
                }
            }
        }
    },
    computed:{
        sobreUmbral: function(){
            return  (this.valor > ((this.validos / 2)+1) );
        },
        bajoUmbral: function(){
            return (this.valor < ( (this.validos / 2) +1 ) );
        }
    },
    methods: {
        formatPrice(value) {
            let val = value;
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")
        }
    },    
    template :'#numero-votos'
})

var comp_pregunta = Vue.component('pregunta',{
    props: ["id","texto", "votos-si", "votos-no", "umbral"],
    components:{
        'votos':comp_voto
    },
    template: '#pregunta-template'
})
