from flask import Blueprint, render_template, request, jsonify


from app.routes.scraperPages.scraperEdenor import inicializarScrap

main_bp = Blueprint('main', __name__)

@main_bp.route("/main")
def index():
    servicios = [
        "Edenor", "Edesur", "Arca", "Telecom", 
        "Natugry", "Arba", "Municipalidad de Tigre"
    ]
    return render_template("index.html", servicios=servicios)

# Metodo que maneja un modal generico y renderiza el contenido segun el tipo de modal
@main_bp.route('/load-modal-content', methods=['GET'])
def load_modal_content():
    modal_type = request.args.get('modalType')
    servicio = request.args.get('servicio', '')
    
    if modal_type == 'config':
        return render_template('components/config_manager.html', servicio=servicio)
    elif modal_type == 'scrap':
        return render_template('components/scrap_manager.html', servicio=servicio)
    elif modal_type == 'configMail':
        return render_template('components/config_mail.html')
    else:
        return jsonify({'error': 'Tipo de modal no reconocido'}), 400
    
@main_bp.route('/get_facturas', methods=['POST'])
def get_facturas():
    servicio = request.json.get('servicio')
    # Aquí haces la lógica para obtener las facturas según el servicio.
    facturas = obtener_facturas(servicio)  # Función que trae las facturas
    return jsonify(facturas)


# Nueva ruta para ejecutar el scraper de Edenor
@main_bp.route('/scraperEdenor', methods=['POST'])
def scraperEdenor():
    servicio= request.json.get('servicio') # El servicio debe ser enviado en el cuerpo de la solicitud

    try:
        if servicio == 'Edenor':
            inicializarScrap() #llama a la funcion del scraper de Edenor
            return jsonify({'status': 'success', 'message': 'Scraper de Edenor ejecutandose correctamente'})
        else:
            return jsonify({'status':'error', 'message': f'Servicio {servicio} no soportado'})
    except Exception as e:
        return jsonify({'status':'error', 'message': str(e)}),500
    