// principal

const URL_DATA_NACIONAL = "http://resultadosconsulta.vanguardia.com/data/nacional.json";
const URL_DATA_DPTO = "http://resultadosconsulta.vanguardia.com/data/dpto.json";
const URL_DATA_DPTO_VAL = "http://resultadosconsulta.vanguardia.com/data/dptoval.json";
const URL_DATA_CAPITALES = "http://resultadosconsulta.vanguardia.com/data/capitales.json";

var consultas = new Vue({ 
    el: '#consultas',
    created: function(){
        this.getDataNac();

        this.interval =setInterval(function () {
            this.getDataNac();
        }.bind(this), 60000);
    },
    methods:{
        getDataNac: function(){
            this.$http.get(URL_DATA_NACIONAL).then( function(response){
                let respuesta = response.body;
                this.pregunta1.votosSI = respuesta.preguntas.pregunta1.votossi;
                this.pregunta1.votosNO = respuesta.preguntas.pregunta1.votosno;
                this.pregunta1.umbral = respuesta.preguntas.pregunta1.votosvalidos;
                this.pregunta2.votosSI = respuesta.preguntas.pregunta2.votossi;
                this.pregunta2.votosNO = respuesta.preguntas.pregunta2.votosno;
                this.pregunta2.umbral = respuesta.preguntas.pregunta2.votosvalidos;
                this.pregunta3.votosSI = respuesta.preguntas.pregunta3.votossi;
                this.pregunta3.votosNO = respuesta.preguntas.pregunta3.votosno;
                this.pregunta3.umbral = respuesta.preguntas.pregunta3.votosvalidos;
                this.pregunta4.votosSI = respuesta.preguntas.pregunta4.votossi;
                this.pregunta4.votosNO = respuesta.preguntas.pregunta4.votosno;
                this.pregunta4.umbral = respuesta.preguntas.pregunta4.votosvalidos;
                this.pregunta5.votosSI = respuesta.preguntas.pregunta5.votossi;
                this.pregunta5.votosNO = respuesta.preguntas.pregunta5.votosno;
                this.pregunta5.umbral = respuesta.preguntas.pregunta5.votosvalidos;
                this.pregunta6.votosSI = respuesta.preguntas.pregunta6.votossi;
                this.pregunta6.votosNO = respuesta.preguntas.pregunta6.votosno;
                this.pregunta6.umbral = respuesta.preguntas.pregunta6.votosvalidos;
                this.pregunta7.votosSI = respuesta.preguntas.pregunta7.votossi;
                this.pregunta7.votosNO = respuesta.preguntas.pregunta7.votosno;
                this.pregunta7.umbral = respuesta.preguntas.pregunta7.votosvalidos;

                this.estadisticas.hora = respuesta.estadisticas.hora;
                this.estadisticas.potsuf = respuesta.estadisticas.potsuf;
                this.estadisticas.porcmesas = respuesta.estadisticas.porcmesas;
                this.estadisticas.boletin = respuesta.estadisticas.boletin;
            });
            
            
        },
        loadMapa: function(){
            let anchoPantalla = window.screen.availWidth;
            if (anchoPantalla > 1012){
                if (this.mapaCargado == 'santander'){
                    this.mapaCargado = 'colombia';
                }else{
                    this.mapaCargado = 'santander';
                }

                this.valDpto={
                    si:0,
                    no:0
                };
                this.dataDpto={
                    Nombre: '',
                    Votos_Validos: 0,
                    Votos_Nulos:0,
                    Votos_No_Marcados:0
                };
                
            }else{
                window.open("http://resultadosconsulta.vanguardia.com/");
            }
        },
        loadDetalleMap: function(dataid){
            
            if (this.mapaCargado == 'santander'){

                var dibujo = document.getElementsByClassName('m'+dataid+' elemmun');
                var nombre_mun = dibujo[0].getAttribute('data-nombre');
                this.dataDpto.Nombre = nombre_mun;

                this.$http.get(URL_DATA_CAPITALES).then(function (response){
                    let respuesta = response.body;
                    let indDatos = "datos"+dataid.toString();
                    let indVal = "valores"+dataid.toString();

                    var datos1 = respuesta["data"][indDatos][dataid][this.selPregunta]

                    this.dataDpto.Votos_Validos = datos1.Votos_Validos;
                    this.dataDpto.Votos_Nulos = datos1.Votos_Nulos
                    this.dataDpto.Votos_No_Marcados = datos1.Votos_No_Marcados

                    var datos2 = respuesta["data"][indDatos][indVal][dataid][this.selPregunta]

                    this.valDpto.si = datos2.si;
                    this.valDpto.no = datos2.no;
             
                })
            }else{
                var dibujo = document.getElementsByClassName('m'+dataid+' elemdep');
                var nombre_mun = dibujo[0].getAttribute('data-nombre');
                this.dataDpto.Nombre = nombre_mun;

                this.$http.get(URL_DATA_DPTO).then(function (response){
                    let respuesta = response.body;
                    let datos_dpto = respuesta.datos[dataid][this.selPregunta];
                    this.dataDpto.Votos_Validos = datos_dpto.Votos_Validos;
                    this.dataDpto.Votos_Nulos = datos_dpto.Votos_Nulos
                    this.dataDpto.Votos_No_Marcados = datos_dpto.Votos_No_Marcados
                })
                this.$http.get(URL_DATA_DPTO_VAL).then(function (response){
                    let respuesta = response.body;
                    let datos_dpto = respuesta.valores[dataid][this.selPregunta];
                    
                    this.valDpto.si = datos_dpto.si;
                    this.valDpto.no = datos_dpto.no;
                })
            }

            
        },
        loadDetalleMapMun: function(dataid){
            
            
        },
        ocultarDatos: function(){
            this.mostarData = false;
        },
        mostarDatos: function(event){
            this.mostarData = true;
        },
        setPregunta: function(num_pregunta){
            this.selPregunta = num_pregunta;
        },
        actualizarCoord: function(event){
            this.mouseX = event.clientX;
            this.mouseY = event.clientY;
            event.preventDefault();
            if (this.mostarData){
                var div = document.getElementById('div_datos_mapa');
                div.style='position:absolute';
                div.style.left = (this.mouseX +25) +'px';
                div.style.top = (this.mouseY+25)+'px';
            }
        },
        formatPrice: function(value) {
            let val = value;
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")
        }
    },
    beforeDestroy: function(){
        clearInterval(this.interval);
    },
    data:{
        mouseX:0,
        mouseY:0,
        mostarData:false,
        selActive:false,
        selPregunta: '001',
        valDpto:{
            si:0,
            no:0
        },
        dataDpto:{
            Nombre: '',
            Votos_Validos: 0,
            Votos_Nulos:0,
            Votos_No_Marcados:0
        },
        mapaCargado: 'santander',
        pregunta1:{
            id: 1,
            texto: 'Reducir el salario de congresistas y altos funcionarios',
            votosSI: 0,
            votosNO: 0,
            umbral: 0
        },
        pregunta2:{
            id:2,
            texto: 'Cárcel a corruptos y prohibirles volver a contratar con el estado',
            votosSI: 0,
            votosNO: 0,
            umbral: 0
        },
        pregunta3:{
            id:3,
            texto: 'Contratación transparente obligatoria en todo el país',
            votosSI: 0,
            votosNO: 0,
            umbral: 0
        },
        pregunta4:{
            id:4,
            texto: 'Presupuestos públicos con participacion de la ciudadanía',
            votosSI: 0,
            votosNO: 0,
            umbral: 0
        },
        pregunta5:{
            id:5,
            texto: 'Congresistas deben rendir cuentas de asistencia y gestión',
            votosSI: 0,
            votosNO: 0,
            umbral: 0
        },
        pregunta6:{
            id:6,
            texto: 'Publicar declaracion de bienes. Aprobar extinción de dominio',
            votosSI: 0,
            votosNO: 0,
            umbral: 0
        },
        pregunta7:{
            id:7,
            texto: 'Máximo 3 periodos en corporaciones públicas',
            votosSI: 0,
            votosNO: 0,
            umbral: 0
        },
        estadisticas: {
            hora: "00:00", 
            potsuf: 0, 
            porcmesas: 0.00, 
            boletin: "0000"
        }
    },
    computed:{
        mostrarMapaSantander: function(){
            return (this.mapaCargado == 'santander')? "display:block": "display:none";
        },
        mostrarMapaColombia: function(){
            return (this.mapaCargado == 'colombia')? "display:block": "display:none";
        },
        small_map: function(){
            return (this.mapaCargado == 'santander')? 'colombia_bt': 'santander_bt';
        },
        label_map: function(){
            return (this.mapaCargado == 'santander')? 'Colombia': 'Santander';
        }
    },
    components:{
        'pregunta': comp_pregunta,
        'estadistica': comp_estadistica,
        'umbralimg': img_umbral
    }
});