from flask import session

TRANSLATIONS = {
    "pt-BR": {
        "nav.system":"SISTEMA","landing.status":"MONITORAMENTO ATIVO","landing.kicker":"SAÚDE • CUIDADO • PREVENÇÃO","landing.hero1":"CUIDE DA","landing.hero2":"SUA","landing.hero3":"SAÚDE.","landing.heart_label":"Coração pulsando com monitoramento cardíaco","landing.beat":"BATIMENTO","landing.continuous":"MONITORAMENTO CONTÍNUO","landing.since":"Desde 2020","landing.pressure":"PRESSÃO","landing.glucose":"GLICEMIA","landing.weight":"PESO","landing.history":"HISTÓRICO",
        "dash.glucose_alert":"Glicemia elevada","dash.water_added":"Água adicionada com sucesso.","dash.underweight":"Abaixo do peso","dash.overweight":"Sobrepeso","dash.obesity_1":"Obesidade grau I","dash.obesity_2":"Obesidade grau II","dash.obesity_3":"Obesidade grau III","dash.bmi_alert":"IMC de {value} indica obesidade. Consulte um médico.",
        "nav.overview":"VISÃO GERAL","nav.calendar":"Calendário","nav.notifications":"Notificações","nav.records":"REGISTROS","nav.ai_short":"Assistente","nav.settings":"Configurações","nav.workspace":"Espaço de saúde","nav.personal_account":"Conta pessoal","nav.personal_area":"Área pessoal",
        "nav.dashboard":"Dashboard","nav.agendamentos":"Agendamentos","nav.prontuario":"Prontuário",
        "nav.consultas":"Consultas","nav.receitas":"Receitas","nav.exames":"Exames","nav.perfil":"Perfil",
        "nav.documentos":"Documentos","nav.ai":"Assistente IA","nav.pdf":"PDF","nav.logout":"Sair",
        "theme.light":"Claro","theme.dark":"Escuro","lang.label":"Idioma","today":"Hoje",
        "ai.title":"Assistente SaúdeApp","ai.subtitle":"Pergunte sobre seus registros ou peça ajuda para organizar sua rotina.",
        "ai.placeholder":"Ex.: quais são minhas próximas consultas?","ai.send":"Enviar",
        "ai.disclaimer":"A IA é apenas informativa e não substitui avaliação de um profissional de saúde.",
        "profile.edit":"Editar perfil","profile.photo":"Foto de perfil",

        "landing.title1":"Sua saúde,","landing.title2":"em um só lugar.",
        "landing.description":"Organize consultas, exames, receitas e informações pessoais de forma simples, prática e segura.",
        "landing.login":"Entrar","landing.register":"Criar cadastro","auth.home":"Voltar à página inicial",
        "landing.note":"Feito para deixar suas informações mais organizadas.",
        "landing.next":"Próxima consulta","landing.organized":"Organizada","landing.allgood":"Tudo em dia",
        "landing.records":"Seus registros","landing.organization":"Organização",
        "landing.information":"Informações reunidas em um só lugar.","landing.tracking":"Acompanhamento",
        "landing.consult_records":"Consulte seus registros quando precisar.","landing.practicality":"Praticidade",
        "landing.easy":"Uma interface simples para facilitar seu dia.",
        "landing.footer":"SaúdeApp · Cuidando da informação para você cuidar da saúde.",

        "login.welcome":"Bem-vindo de volta","login.subtitle":"Entre na sua conta do SaúdeApp",
        "login.label":"Login","login.login_placeholder":"Digite seu login","login.password":"Senha",
        "login.password_placeholder":"Digite sua senha","login.forgot":"Esqueci minha senha",
        "login.remember":"Lembrar de mim","login.enter":"Entrar","login.loading":"Entrando...",
        "login.no_account":"Não tem uma conta?","login.create":"Criar minha conta",
        "login.security":"Seus dados são protegidos localmente","login.show":"Mostrar senha","login.hide":"Ocultar senha",
        "login.future":"Função disponível em uma versão futura",

        "register.title":"Criar conta","register.fullname":"Nome completo","register.age":"Idade",
        "register.height":"Altura (m)","register.weight":"Peso (kg)","register.blood":"Tipo sanguíneo",
        "register.water":"Meta de água diária (L)","register.create":"Cadastrar",
        "register.have":"Já tem conta?","register.enter":"Entrar",

        "dash.hello":"Olá,","dash.assistant":"Assistente IA","dash.bmi":"IMC","dash.weight":"Peso atual",
        "dash.last_pressure":"Pressão (última)","dash.last_glucose":"Glicemia (última)","dash.height":"Altura:",
        "dash.avg30":"Média 30d:","dash.hydration":"Hidratação","dash.add":"Adicionar","dash.reset":"Resetar dia",
        "dash.register_weight":"Registrar Peso","dash.register_pressure":"Registrar Pressão","dash.register_glucose":"Registrar Glicemia",
        "dash.save":"Salvar","dash.weight_evolution":"Evolução do Peso","dash.pressure":"Pressão Arterial",
        "dash.glucose":"Glicemia","dash.diastolic":"Diastólica","dash.systolic":"Sistólica",
        "dash.overview":"VISÃO GERAL","dash.summary":"Resumo do seu acompanhamento em","dash.today":"Hoje","dash.pressure_alert":"Pressão arterial elevada","dash.hydration_alert":"Você atingiu apenas 25.0% da meta de hidratação.","dash.open_assistant":"Abrir assistente","dash.normal_weight":"Peso normal","dash.no_trend":"Sem tendência suficiente","dash.days30":"em 30 dias","dash.no_average":"Sem média disponível","dash.no_records":"Sem registros","dash.today_label":"HOJE","dash.evolution":"EVOLUÇÃO","dash.records_count":"registros","dash.last7":"Últimos 7 dias","dash.consumed":"consumidos","dash.goal":"Meta","dash.quick_record":"REGISTRO RÁPIDO","dash.update_tracking":"Atualizar acompanhamento","dash.save_record":"Salvar registro","dash.weight_kg":"Peso (kg)","dash.pressure_arterial":"Pressão arterial","dash.glucose_mg":"Glicemia (mg/dL)","dash.pressure_chart":"Pressão arterial","dash.weight_chart":"Peso","dash.glucose_chart":"Glicemia","dash.no_records_yet":"Nenhum registro ainda.",

        "common.doctor":"Médico","common.crm":"CRM","common.specialty":"Especialidade","common.date":"Data",
        "common.time":"Horário","common.location":"Local","common.notes":"Observações","common.diagnosis":"Diagnóstico",
        "common.history":"Histórico","common.pdf":"PDF","common.save":"Salvar","common.cancel":"Cancelar",
        "common.confirm":"Confirmar","common.add":"Adicionar","common.remove":"Remover","common.status":"Status",
        "common.none":"Nenhum registro ainda.","common.yes_done":"Realizada","common.cancelled":"Cancelada",

        "appointments.title":"Agendamentos de Consulta","appointments.new":"Marcar nova consulta",
        "appointments.upcoming":"Próximas consultas","appointments.history":"Histórico de agendamentos",
        "appointments.schedule":"Agendar","appointments.place":"Ex: Clínica Central, sala 4",
        "appointments.future":"Escolha um horário futuro.","appointments.complete":"Concluir consulta",
        "appointments.complete_note":"Isso vai adicionar um registro ao seu prontuário.",
        "appointments.cancel_confirm":"Cancelar este agendamento?","appointments.empty":"Nenhuma consulta agendada.",

        "consultations.title":"Consultas Médicas","consultations.new":"Nova consulta",
        "consultations.add":"Adicionar","consultations.empty":"Nenhuma consulta registrada ainda.",

        "prescriptions.title":"Receitas Médicas","prescriptions.new":"Nova receita","prescriptions.meds":"Medicamentos",
        "prescriptions.add_med":"+ Medicamento","prescriptions.save":"Salvar receita","prescriptions.empty":"Nenhuma receita registrada ainda.",
        "prescriptions.name":"Nome","prescriptions.dose":"Dosagem","prescriptions.frequency":"Frequência","prescriptions.duration":"Duração",

        "exams.title":"Exames","exams.register":"Registrar exame","exams.type":"Tipo de exame",
        "exams.file":"Arquivo (PDF/PNG/JPG)","exams.result":"Resultado principal","exams.save":"Salvar exame",
        "exams.view":"Ver","exams.empty":"Nenhum exame registrado ainda.",

        "docs.title":"Central de documentos","docs.academic":"SIMULAÇÃO ACADÊMICA",
        "docs.subtitle":"Documentos com aparência profissional",
        "docs.description":"Gere PDFs organizados para demonstrar como um sistema de saúde pode produzir comprovantes e registros.",
        "docs.summary":"Resumo de saúde","docs.card":"Carteirinha","docs.available":"Nenhum registro disponível.",

        "record.title":"Prontuário Eletrônico","record.summary":"Resumo clínico",
        "record.allergies":"Alergias (separadas por vírgula)","record.chronic":"Doenças crônicas",
        "record.continuous":"Medicamentos de uso contínuo","record.save":"Salvar resumo clínico",
        "record.timeline":"Linha do tempo clínica","record.empty":"Nenhum evento clínico registrado ainda. Consultas, exames e receitas aparecerão aqui automaticamente.",

        "profile.title":"Meu Perfil","profile.name":"Nome","profile.login":"Login","profile.age":"Idade",
        "profile.blood":"Tipo sanguíneo","profile.height":"Altura","profile.weight":"Peso","profile.bmi":"IMC",
        "profile.water":"Meta de água","profile.notes":"Observações","profile.delete":"Excluir conta",
        "profile.delete_confirm":"Tem certeza? Esta ação é irreversível.",
        "profile.edit_title":"Editar Perfil","profile.choose_photo":"Escolha uma imagem JPG, PNG ou WEBP.",
        "profile.save":"Salvar",

        "ai.question":"Pergunta","ai.next":"Próximas consultas","ai.summary":"Resumo",
        "ai.important":"Informação importante",
        "ai.privacy":"O assistente recebe apenas os dados de saúde necessários para responder dentro desta sessão. Não envie senhas ou informações que não sejam necessárias.",

        "verify.title":"Verificação","verify.found":"Registro encontrado",
        "verify.token":"Token:","verify.type":"Tipo:","verify.issued":"Emitido em:",
        "verify.warning":"Este sistema é uma simulação acadêmica. Esta página não comprova autenticidade de documento médico real.",
        "error.title":"Algo não saiu como esperado","error.home":"Voltar ao início",

        "footer.academic":"Projeto acadêmico","footer.local":"Dados locais",
    },
    "en": {
        "nav.system":"SYSTEM","landing.status":"ACTIVE MONITORING","landing.kicker":"HEALTH • CARE • PREVENTION","landing.hero1":"TAKE CARE OF","landing.hero2":"YOUR","landing.hero3":"HEALTH.","landing.heart_label":"Pulsing heart with cardiac monitoring","landing.beat":"HEARTBEAT","landing.continuous":"CONTINUOUS MONITORING","landing.since":"Since 2020","landing.pressure":"BLOOD PRESSURE","landing.glucose":"GLUCOSE","landing.weight":"WEIGHT","landing.history":"HISTORY",
        "dash.glucose_alert":"High blood glucose","dash.water_added":"Water added successfully.","dash.underweight":"Underweight","dash.overweight":"Overweight","dash.obesity_1":"Obesity class I","dash.obesity_2":"Obesity class II","dash.obesity_3":"Obesity class III","dash.bmi_alert":"BMI of {value} indicates obesity. Consult a doctor.",
        "nav.overview":"OVERVIEW","nav.calendar":"Calendar","nav.notifications":"Notifications","nav.records":"RECORDS","nav.ai_short":"Assistant","nav.settings":"Settings","nav.workspace":"Health workspace","nav.personal_account":"Personal account","nav.personal_area":"Personal area",
        "nav.dashboard":"Dashboard","nav.agendamentos":"Appointments","nav.prontuario":"Medical record",
        "nav.consultas":"Visits","nav.receitas":"Prescriptions","nav.exames":"Exams","nav.perfil":"Profile",
        "nav.documentos":"Documents","nav.ai":"AI Assistant","nav.pdf":"PDF","nav.logout":"Log out",
        "theme.light":"Light","theme.dark":"Dark","lang.label":"Language","today":"Today",
        "ai.title":"HealthApp Assistant","ai.subtitle":"Ask about your records or get help organizing your routine.",
        "ai.placeholder":"Example: what are my next appointments?","ai.send":"Send",
        "ai.disclaimer":"AI is informational only and does not replace evaluation by a healthcare professional.",
        "profile.edit":"Edit profile","profile.photo":"Profile picture",

        "landing.title1":"Your health,","landing.title2":"all in one place.",
        "landing.description":"Organize appointments, exams, prescriptions and personal information in a simple, practical and secure way.",
        "landing.login":"Log in","landing.register":"Create account","landing.note":"Made to keep your information organized.",
        "landing.next":"Next appointment","landing.organized":"Organized","landing.allgood":"All up to date",
        "landing.records":"Your records","landing.organization":"Organization","landing.information":"Information in one place.",
        "landing.tracking":"Tracking","landing.consult_records":"Check your records whenever you need.",
        "landing.practicality":"Practicality","landing.easy":"A simple interface to make your day easier.",
        "landing.footer":"HealthApp · Taking care of information so you can take care of your health.",

        "login.welcome":"Welcome back","login.subtitle":"Sign in to your HealthApp account","login.label":"Login",
        "login.login_placeholder":"Enter your login","login.password":"Password","login.password_placeholder":"Enter your password",
        "login.forgot":"Forgot my password","login.remember":"Remember me","login.enter":"Log in","login.loading":"Signing in...",
        "login.no_account":"Don't have an account?","login.create":"Create my account","login.security":"Your data is protected locally",
        "login.show":"Show password","login.hide":"Hide password","login.future":"Feature available in a future version",

        "register.title":"Create account","register.fullname":"Full name","register.age":"Age","register.height":"Height (m)",
        "register.weight":"Weight (kg)","register.blood":"Blood type","register.water":"Daily water goal (L)",
        "register.create":"Sign up","register.have":"Already have an account?","register.enter":"Log in",

        "dash.hello":"Hello,","dash.assistant":"AI Assistant","dash.bmi":"BMI","dash.weight":"Current weight",
        "dash.last_pressure":"Latest blood pressure","dash.last_glucose":"Latest glucose","dash.height":"Height:",
        "dash.avg30":"30-day average:","dash.hydration":"Hydration","dash.add":"Add","dash.reset":"Reset day",
        "dash.register_weight":"Record Weight","dash.register_pressure":"Record Blood Pressure","dash.register_glucose":"Record Glucose",
        "dash.save":"Save","dash.weight_evolution":"Weight Progress","dash.pressure":"Blood Pressure","dash.glucose":"Glucose",
        "dash.diastolic":"Diastolic","dash.systolic":"Systolic",
        "dash.overview":"OVERVIEW","dash.summary":"Summary of your health tracking on","dash.today":"Today","dash.pressure_alert":"High blood pressure","dash.hydration_alert":"You reached only 25.0% of your hydration goal.","dash.open_assistant":"Open assistant","dash.normal_weight":"Normal weight","dash.no_trend":"Not enough trend data","dash.days30":"in 30 days","dash.no_average":"No average available","dash.no_records":"No records","dash.today_label":"TODAY","dash.evolution":"EVOLUTION","dash.records_count":"records","dash.last7":"Last 7 days","dash.consumed":"consumed","dash.goal":"Goal","dash.quick_record":"QUICK ENTRY","dash.update_tracking":"Update tracking","dash.save_record":"Save record","dash.weight_kg":"Weight (kg)","dash.pressure_arterial":"Blood pressure","dash.glucose_mg":"Blood glucose (mg/dL)","dash.pressure_chart":"Blood pressure","dash.weight_chart":"Weight","dash.glucose_chart":"Blood glucose","dash.no_records_yet":"No records yet.",


        "common.doctor":"Doctor","common.crm":"CRM","common.specialty":"Specialty","common.date":"Date","common.time":"Time",
        "common.location":"Location","common.notes":"Notes","common.diagnosis":"Diagnosis","common.history":"History","common.pdf":"PDF",
        "common.save":"Save","common.cancel":"Cancel","common.confirm":"Confirm","common.add":"Add","common.remove":"Remove",
        "common.status":"Status","common.none":"No records yet.","common.yes_done":"Completed","common.cancelled":"Cancelled",

        "appointments.title":"Appointments","appointments.new":"Schedule a new appointment","appointments.upcoming":"Upcoming appointments",
        "appointments.history":"Appointment history","appointments.schedule":"Schedule","appointments.place":"Example: Central Clinic, room 4",
        "appointments.future":"Choose a future time.","appointments.complete":"Complete appointment",
        "appointments.complete_note":"This will add a record to your medical record.","appointments.cancel_confirm":"Cancel this appointment?",
        "appointments.empty":"No appointments scheduled.",

        "consultations.title":"Medical Visits","consultations.new":"New visit","consultations.add":"Add",
        "consultations.empty":"No visits recorded yet.",

        "prescriptions.title":"Prescriptions","prescriptions.new":"New prescription","prescriptions.meds":"Medications",
        "prescriptions.add_med":"+ Medication","prescriptions.save":"Save prescription","prescriptions.empty":"No prescriptions recorded yet.",
        "prescriptions.name":"Name","prescriptions.dose":"Dosage","prescriptions.frequency":"Frequency","prescriptions.duration":"Duration",

        "exams.title":"Exams","exams.register":"Record exam","exams.type":"Exam type","exams.file":"File (PDF/PNG/JPG)",
        "exams.result":"Main result","exams.save":"Save exam","exams.view":"View","exams.empty":"No exams recorded yet.",

        "docs.title":"Document center","docs.academic":"ACADEMIC SIMULATION","docs.subtitle":"Professional-looking documents",
        "docs.description":"Generate organized PDFs to demonstrate how a health system can produce records and receipts.",
        "docs.summary":"Health summary","docs.card":"Patient card","docs.available":"No records available.",

        "record.title":"Electronic Medical Record","record.summary":"Clinical summary","record.allergies":"Allergies (comma-separated)",
        "record.chronic":"Chronic conditions","record.continuous":"Continuous medications","record.save":"Save clinical summary",
        "record.timeline":"Clinical timeline","record.empty":"No clinical events recorded yet. Visits, exams and prescriptions will appear here automatically.",

        "profile.title":"My Profile","profile.name":"Name","profile.login":"Login","profile.age":"Age","profile.blood":"Blood type",
        "profile.height":"Height","profile.weight":"Weight","profile.bmi":"BMI","profile.water":"Water goal","profile.notes":"Notes",
        "profile.delete":"Delete account","profile.delete_confirm":"Are you sure? This action cannot be undone.",
        "profile.edit_title":"Edit Profile","profile.choose_photo":"Choose a JPG, PNG or WEBP image.","profile.save":"Save",

        "ai.question":"Question","ai.next":"Next appointments","ai.summary":"Summary","ai.important":"Important information",
        "ai.privacy":"The assistant receives only the health data needed to answer during this session. Do not send passwords or unnecessary information.",

        "verify.title":"Verification","verify.found":"Record found","verify.token":"Token:","verify.type":"Type:","verify.issued":"Issued on:",
        "verify.warning":"This system is an academic simulation. This page does not prove the authenticity of a real medical document.",
        "error.title":"Something went wrong","error.home":"Back to home","footer.academic":"Academic project","footer.local":"Local data",
    },
    "es": {
        "nav.system":"SISTEMA","landing.status":"MONITOREO ACTIVO","landing.kicker":"SALUD • CUIDADO • PREVENCIÓN","landing.hero1":"CUIDA DE","landing.hero2":"TU","landing.hero3":"SALUD.","landing.heart_label":"Corazón latiendo con monitoreo cardíaco","landing.beat":"LATIDO","landing.continuous":"MONITOREO CONTINUO","landing.since":"Desde 2020","landing.pressure":"PRESIÓN","landing.glucose":"GLUCEMIA","landing.weight":"PESO","landing.history":"HISTORIAL",
        "dash.glucose_alert":"Glucemia alta","dash.water_added":"Agua añadida correctamente.","dash.underweight":"Bajo peso","dash.overweight":"Sobrepeso","dash.obesity_1":"Obesidad grado I","dash.obesity_2":"Obesidad grado II","dash.obesity_3":"Obesidad grado III","dash.bmi_alert":"El IMC de {value} indica obesidad. Consulta a un médico.",
        "nav.overview":"VISTA GENERAL","nav.calendar":"Calendario","nav.notifications":"Notificaciones","nav.records":"REGISTROS","nav.ai_short":"Asistente","nav.settings":"Configuración","nav.workspace":"Espacio de salud","nav.personal_account":"Cuenta personal","nav.personal_area":"Área personal",
        "nav.dashboard":"Panel","nav.agendamentos":"Citas","nav.prontuario":"Historial médico","nav.consultas":"Consultas",
        "nav.receitas":"Recetas","nav.exames":"Exámenes","nav.perfil":"Perfil","nav.documentos":"Documentos","nav.ai":"Asistente IA",
        "nav.pdf":"PDF","nav.logout":"Salir","theme.light":"Claro","theme.dark":"Oscuro","lang.label":"Idioma","today":"Hoy",
        "ai.title":"Asistente SaludApp","ai.subtitle":"Pregunta sobre tus registros o pide ayuda para organizar tu rutina.",
        "ai.placeholder":"Ej.: ¿cuáles son mis próximas citas?","ai.send":"Enviar",
        "ai.disclaimer":"La IA es solo informativa y no sustituye la evaluación de un profesional de salud.",
        "profile.edit":"Editar perfil","profile.photo":"Foto de perfil",
        "landing.title1":"Tu salud,","landing.title2":"en un solo lugar.",
        "landing.description":"Organiza citas, exámenes, recetas e información personal de forma sencilla, práctica y segura.",
        "landing.login":"Entrar","landing.register":"Crear cuenta","landing.note":"Hecho para mantener tu información organizada.",
        "landing.next":"Próxima cita","landing.organized":"Organizada","landing.allgood":"Todo al día","landing.records":"Tus registros",
        "landing.organization":"Organización","landing.information":"Información reunida en un solo lugar.","landing.tracking":"Seguimiento",
        "landing.consult_records":"Consulta tus registros cuando lo necesites.","landing.practicality":"Practicidad",
        "landing.easy":"Una interfaz sencilla para facilitar tu día.","landing.footer":"SaludApp · Cuidando la información para cuidar tu salud.",
        "login.welcome":"Bienvenido de nuevo","login.subtitle":"Entra en tu cuenta de SaludApp","login.label":"Usuario",
        "login.login_placeholder":"Escribe tu usuario","login.password":"Contraseña","login.password_placeholder":"Escribe tu contraseña",
        "login.forgot":"Olvidé mi contraseña","login.remember":"Recordarme","login.enter":"Entrar","login.loading":"Entrando...",
        "login.no_account":"¿No tienes una cuenta?","login.create":"Crear mi cuenta","login.security":"Tus datos están protegidos localmente",
        "login.show":"Mostrar contraseña","login.hide":"Ocultar contraseña","login.future":"Función disponible en una versión futura",
        "register.title":"Crear cuenta","register.fullname":"Nombre completo","register.age":"Edad","register.height":"Altura (m)",
        "register.weight":"Peso (kg)","register.blood":"Tipo de sangre","register.water":"Meta diaria de agua (L)",
        "register.create":"Registrarse","register.have":"¿Ya tienes una cuenta?","register.enter":"Entrar",
        "dash.hello":"Hola,","dash.assistant":"Asistente IA","dash.bmi":"IMC","dash.weight":"Peso actual",
        "dash.last_pressure":"Última presión","dash.last_glucose":"Última glucemia","dash.height":"Altura:",
        "dash.avg30":"Promedio 30 días:","dash.hydration":"Hidratación","dash.add":"Añadir","dash.reset":"Reiniciar día",
        "dash.register_weight":"Registrar Peso","dash.register_pressure":"Registrar Presión","dash.register_glucose":"Registrar Glucemia",
        "dash.save":"Guardar","dash.weight_evolution":"Evolución del Peso","dash.pressure":"Presión Arterial","dash.glucose":"Glucemia",
        "dash.diastolic":"Diastólica","dash.systolic":"Sistólica",
        "dash.overview":"VISTA GENERAL","dash.summary":"Resumen de tu seguimiento el","dash.today":"Hoy","dash.pressure_alert":"Presión arterial alta","dash.hydration_alert":"Has alcanzado solo el 25.0% de tu meta de hidratación.","dash.open_assistant":"Abrir asistente","dash.normal_weight":"Peso normal","dash.no_trend":"Tendencia insuficiente","dash.days30":"en 30 días","dash.no_average":"Sin promedio disponible","dash.no_records":"Sin registros","dash.today_label":"HOY","dash.evolution":"EVOLUCIÓN","dash.records_count":"registros","dash.last7":"Últimos 7 días","dash.consumed":"consumidos","dash.goal":"Meta","dash.quick_record":"REGISTRO RÁPIDO","dash.update_tracking":"Actualizar seguimiento","dash.save_record":"Guardar registro","dash.weight_kg":"Peso (kg)","dash.pressure_arterial":"Presión arterial","dash.glucose_mg":"Glucemia (mg/dL)","dash.pressure_chart":"Presión arterial","dash.weight_chart":"Peso","dash.glucose_chart":"Glucemia","dash.no_records_yet":"Aún no hay registros.",
        "common.doctor":"Médico","common.crm":"CRM","common.specialty":"Especialidad","common.date":"Fecha","common.time":"Hora",
        "common.location":"Lugar","common.notes":"Observaciones","common.diagnosis":"Diagnóstico","common.history":"Historial",
        "common.pdf":"PDF","common.save":"Guardar","common.cancel":"Cancelar","common.confirm":"Confirmar","common.add":"Añadir",
        "common.remove":"Eliminar","common.status":"Estado","common.none":"Aún no hay registros.","common.yes_done":"Realizada","common.cancelled":"Cancelada",
        "appointments.title":"Citas médicas","appointments.new":"Programar una nueva cita","appointments.upcoming":"Próximas citas",
        "appointments.history":"Historial de citas","appointments.schedule":"Programar","appointments.place":"Ej.: Clínica Central, sala 4",
        "appointments.future":"Elige una hora futura.","appointments.complete":"Completar cita",
        "appointments.complete_note":"Esto añadirá un registro a tu historial médico.","appointments.cancel_confirm":"¿Cancelar esta cita?",
        "appointments.empty":"No hay citas programadas.",
        "consultations.title":"Consultas Médicas","consultations.new":"Nueva consulta","consultations.add":"Añadir",
        "consultations.empty":"No hay consultas registradas.",
        "prescriptions.title":"Recetas Médicas","prescriptions.new":"Nueva receta","prescriptions.meds":"Medicamentos",
        "prescriptions.add_med":"+ Medicamento","prescriptions.save":"Guardar receta","prescriptions.empty":"No hay recetas registradas.",
        "prescriptions.name":"Nombre","prescriptions.dose":"Dosis","prescriptions.frequency":"Frecuencia","prescriptions.duration":"Duración",
        "exams.title":"Exámenes","exams.register":"Registrar examen","exams.type":"Tipo de examen","exams.file":"Archivo (PDF/PNG/JPG)",
        "exams.result":"Resultado principal","exams.save":"Guardar examen","exams.view":"Ver","exams.empty":"No hay exámenes registrados.",
        "docs.title":"Centro de documentos","docs.academic":"SIMULACIÓN ACADÉMICA","docs.subtitle":"Documentos con apariencia profesional",
        "docs.description":"Genera PDFs organizados para demostrar cómo un sistema de salud puede producir comprobantes y registros.",
        "docs.summary":"Resumen de salud","docs.card":"Carné","docs.available":"No hay registros disponibles.",
        "record.title":"Historial Médico Electrónico","record.summary":"Resumen clínico","record.allergies":"Alergias (separadas por comas)",
        "record.chronic":"Enfermedades crónicas","record.continuous":"Medicamentos de uso continuo","record.save":"Guardar resumen clínico",
        "record.timeline":"Línea de tiempo clínica","record.empty":"Aún no hay eventos clínicos. Las consultas, exámenes y recetas aparecerán aquí automáticamente.",
        "profile.title":"Mi Perfil","profile.name":"Nombre","profile.login":"Usuario","profile.age":"Edad","profile.blood":"Tipo de sangre",
        "profile.height":"Altura","profile.weight":"Peso","profile.bmi":"IMC","profile.water":"Meta de agua","profile.notes":"Observaciones",
        "profile.delete":"Eliminar cuenta","profile.delete_confirm":"¿Estás seguro? Esta acción es irreversible.","profile.edit_title":"Editar Perfil",
        "profile.choose_photo":"Elige una imagen JPG, PNG o WEBP.","profile.save":"Guardar",
        "ai.question":"Pregunta","ai.next":"Próximas citas","ai.summary":"Resumen","ai.important":"Información importante",
        "ai.privacy":"El asistente recibe solo los datos de salud necesarios para responder durante esta sesión. No envíes contraseñas ni información innecesaria.",
        "verify.title":"Verificación","verify.found":"Registro encontrado","verify.token":"Token:","verify.type":"Tipo:","verify.issued":"Emitido el:",
        "verify.warning":"Este sistema es una simulación académica. Esta página no demuestra la autenticidad de un documento médico real.",
        "error.title":"Algo salió mal","error.home":"Volver al inicio","footer.academic":"Proyecto académico","footer.local":"Datos locales",
    }
}


TRANSLATIONS["pt-BR"].update({
    "nav.gamification":"Progresso",
    "game.title":"Meu progresso", "game.eyebrow":"CONSTÂNCIA", "game.subtitle":"Acompanhe sua evolução no uso do SaúdeApp. XP recompensa registros e constância, não resultados clínicos.",
    "game.level":"NÍVEL", "game.next_level":"Próximo nível", "game.days":"dias", "game.streak":"sequência atual", "game.open":"Ver progresso",
    "game.progress":"PROGRESSO", "game.to_next":"para o próximo nível", "game.this_level":"neste nível", "game.level_total":"para avançar", "game.current_streak":"dias seguidos", "game.best":"recorde",
    "game.actions":"Ações registradas", "game.actions_desc":"atividades que geraram XP", "game.water_days":"Dias com meta de água", "game.water_desc":"dias em que a meta foi registrada como alcançada", "game.badges":"Conquistas", "game.badges_desc":"marcos desbloqueados",
    "game.achievements":"CONQUISTAS", "game.unlocked":"Desbloqueadas", "game.goals":"PRÓXIMOS MARCOS", "game.next_badges":"Ainda bloqueadas", "game.no_badges":"Faça seus primeiros registros para desbloquear conquistas.",
    "game.history":"HISTÓRICO", "game.recent":"Atividade recente", "game.no_activity":"Nenhuma atividade registrada ainda.", "game.daily":"HOJE", "game.missions":"Missões do dia", "game.refreshes":"Atualizadas conforme você registra atividades", "game.note":"O sistema foi desenhado para incentivar acompanhamento e organização. Ele não premia perda de peso, valores de exames ou outras metas clínicas específicas.",
})
TRANSLATIONS["en"].update({
    "nav.gamification":"Progress", "game.title":"My progress", "game.eyebrow":"CONSISTENCY", "game.subtitle":"Track your progress using SaúdeApp. XP rewards logging and consistency, not clinical outcomes.", "game.level":"LEVEL", "game.next_level":"Next level", "game.days":"days", "game.streak":"current streak", "game.open":"View progress", "game.progress":"PROGRESS", "game.to_next":"to next level", "game.this_level":"at this level", "game.level_total":"to advance", "game.current_streak":"consecutive days", "game.best":"best", "game.actions":"Logged actions", "game.actions_desc":"activities that earned XP", "game.water_days":"Water-goal days", "game.water_desc":"days with the goal recorded as reached", "game.badges":"Achievements", "game.badges_desc":"unlocked milestones", "game.achievements":"ACHIEVEMENTS", "game.unlocked":"Unlocked", "game.goals":"NEXT MILESTONES", "game.next_badges":"Still locked", "game.no_badges":"Make your first entries to unlock achievements.", "game.history":"HISTORY", "game.recent":"Recent activity", "game.no_activity":"No activity recorded yet.", "game.daily":"TODAY", "game.missions":"Daily missions", "game.refreshes":"Updated as you log activities", "game.note":"The system rewards tracking and organization. It does not reward weight loss, test values, or specific clinical outcomes."
})
TRANSLATIONS["es"].update({
    "nav.gamification":"Progreso", "game.title":"Mi progreso", "game.eyebrow":"CONSTANCIA", "game.subtitle":"Acompaña tu evolución usando SaludApp. La XP recompensa registros y constancia, no resultados clínicos.", "game.level":"NIVEL", "game.next_level":"Siguiente nivel", "game.days":"días", "game.streak":"racha actual", "game.open":"Ver progreso", "game.progress":"PROGRESO", "game.to_next":"para el siguiente nivel", "game.this_level":"en este nivel", "game.level_total":"para avanzar", "game.current_streak":"días consecutivos", "game.best":"récord", "game.actions":"Acciones registradas", "game.actions_desc":"actividades que generaron XP", "game.water_days":"Días con meta de agua", "game.water_desc":"días en que la meta quedó registrada como alcanzada", "game.badges":"Logros", "game.badges_desc":"hitos desbloqueados", "game.achievements":"LOGROS", "game.unlocked":"Desbloqueados", "game.goals":"PRÓXIMOS HITOS", "game.next_badges":"Aún bloqueados", "game.no_badges":"Haz tus primeros registros para desbloquear logros.", "game.history":"HISTORIAL", "game.recent":"Actividad reciente", "game.no_activity":"Aún no hay actividad registrada.", "game.daily":"HOY", "game.missions":"Misiones del día", "game.refreshes":"Se actualizan al registrar actividades", "game.note":"El sistema recompensa el seguimiento y la organización. No recompensa la pérdida de peso, valores de exámenes ni resultados clínicos específicos."
})

TRANSLATIONS["pt-BR"].update({
    "register.kicker":"CONFIGURAÇÃO INICIAL", "register.hero_title":"Seu acompanhamento começa aqui.",
    "register.hero_text":"Crie seu espaço pessoal para organizar registros, consultas e evolução em um só lugar.",
    "register.point1":"Seus registros ficam organizados", "register.point2":"Acompanhe sua rotina ao longo do tempo", "register.point3":"Desbloqueie progresso conforme participa",
    "register.academic":"Projeto acadêmico · dados locais", "register.step":"ETAPA 01 DE 02", "register.form_subtitle":"Preencha seus dados básicos para começar.",
    "register.account_section":"Sua conta", "register.account_hint":"Escolha como você vai acessar o SaúdeApp.", "register.password_hint":"Mínimo de 8 caracteres",
    "register.health_section":"Dados básicos", "register.health_hint":"Essas informações ajudam a organizar seu acompanhamento.",
    "register.data_note":"Seus dados são usados pelo projeto para montar seu acompanhamento pessoal e ficam armazenados localmente.", "register.water_unit":"L / dia",
    "game.weekly":"ESTA SEMANA", "game.weekly_title":"Missões semanais", "game.weekly_note":"Cada missão concluída rende XP. Ao completar as três, você recebe um bônus extra de 100 XP.",
    "game.tree_eyebrow":"ÁRVORE DE PROGRESSO", "game.tree_title":"Construa seu histórico", "game.tree_subtitle":"Cada área evolui conforme você registra atividades.",
    "game.rewards":"Recompensas", "game.rewards_desc":"desbloqueios por nível", "game.rewards_eyebrow":"RECOMPENSAS", "game.rewards_title":"Próximos desbloqueios", "game.rewards_subtitle":"Continue avançando para liberar novos títulos e temas."
})
TRANSLATIONS["en"].update({
    "register.kicker":"INITIAL SETUP", "register.hero_title":"Your tracking starts here.", "register.hero_text":"Create your personal space to organize records, appointments and progress in one place.",
    "register.point1":"Keep your records organized", "register.point2":"Follow your routine over time", "register.point3":"Unlock progress as you participate", "register.academic":"Academic project · local data",
    "register.step":"STEP 01 OF 02", "register.form_subtitle":"Fill in your basic information to get started.", "register.account_section":"Your account", "register.account_hint":"Choose how you will access SaúdeApp.", "register.password_hint":"Minimum 8 characters",
    "register.health_section":"Basic information", "register.health_hint":"These details help organize your tracking.", "register.data_note":"Your data is used by the project for your personal tracking and is stored locally.", "register.water_unit":"L / day",
    "game.weekly":"THIS WEEK", "game.weekly_title":"Weekly missions", "game.weekly_note":"Each completed mission grants XP. Complete all three to receive an extra 100 XP bonus.", "game.tree_eyebrow":"PROGRESS TREE", "game.tree_title":"Build your history", "game.tree_subtitle":"Each area grows as you log activities.",
    "game.rewards":"Rewards", "game.rewards_desc":"level unlocks", "game.rewards_eyebrow":"REWARDS", "game.rewards_title":"Next unlocks", "game.rewards_subtitle":"Keep progressing to unlock new titles and themes."
})
TRANSLATIONS["es"].update({
    "register.kicker":"CONFIGURACIÓN INICIAL", "register.hero_title":"Tu seguimiento comienza aquí.", "register.hero_text":"Crea tu espacio personal para organizar registros, citas y evolución en un solo lugar.",
    "register.point1":"Mantén tus registros organizados", "register.point2":"Acompaña tu rutina con el tiempo", "register.point3":"Desbloquea progreso al participar", "register.academic":"Proyecto académico · datos locales",
    "register.step":"ETAPA 01 DE 02", "register.form_subtitle":"Completa tus datos básicos para comenzar.", "register.account_section":"Tu cuenta", "register.account_hint":"Elige cómo accederás a SaúdeApp.", "register.password_hint":"Mínimo 8 caracteres",
    "register.health_section":"Datos básicos", "register.health_hint":"Estos datos ayudan a organizar tu seguimiento.", "register.data_note":"Tus datos se utilizan para tu seguimiento personal y se almacenan localmente.", "register.water_unit":"L / día",
    "game.weekly":"ESTA SEMANA", "game.weekly_title":"Misiones semanales", "game.weekly_note":"Cada misión completada otorga XP. Completa las tres para recibir 100 XP adicionales.", "game.tree_eyebrow":"ÁRBOL DE PROGRESO", "game.tree_title":"Construye tu historial", "game.tree_subtitle":"Cada área crece según registras actividades.",
    "game.rewards":"Recompensas", "game.rewards_desc":"desbloqueos por nivel", "game.rewards_eyebrow":"RECOMPENSAS", "game.rewards_title":"Próximos desbloqueos", "game.rewards_subtitle":"Sigue avanzando para desbloquear nuevos títulos y temas."
})



# Traduções das telas adicionadas na versão 3.x.
_EXTRA_TRANSLATIONS = {
    "pt-BR": {
        "settings.eyebrow":"SISTEMA", "settings.title":"Configurações", "settings.subtitle":"Controle sua conta, privacidade e preferências.",
        "settings.account":"Conta", "settings.account_hint":"Segurança de acesso", "settings.current_password":"Senha atual", "settings.new_password":"Nova senha", "settings.change_password":"Alterar senha",
        "settings.preferences":"Preferências", "settings.preferences_hint":"Idioma e aparência", "settings.language":"Idioma", "settings.language_hint":"Altere pelo seletor no canto inferior da interface.", "settings.theme":"Tema", "settings.theme_hint":"Escolha entre claro e escuro.",
        "settings.data":"Seus dados", "settings.data_hint":"Portabilidade", "settings.data_text":"Baixe uma cópia dos seus registros em formato aberto para guardar ou analisar.", "settings.export":"Exportar meus dados", "settings.export_pdf":"Baixar relatório em PDF",
        "settings.danger":"Zona de risco", "settings.danger_hint":"Operações irreversíveis", "settings.danger_text":"Excluir a conta remove seus registros do banco local.", "settings.delete":"Excluir minha conta", "settings.delete_confirm":"Tem certeza? Esta ação é irreversível.",
        "notifications.eyebrow":"CENTRAL", "notifications.title":"Notificações", "notifications.subtitle":"Alertas e lembretes importantes do seu acompanhamento.", "notifications.mark_all":"Marcar todas como lidas", "notifications.mark_read":"Marcar lida", "notifications.empty_title":"Tudo em dia.", "notifications.empty_text":"Não há notificações no momento.",
        "calendar.eyebrow":"AGENDA", "calendar.title":"Calendário", "calendar.subtitle":"Visualize suas consultas futuras em um só lugar.", "calendar.previous":"Anterior", "calendar.today":"Hoje", "calendar.next":"Próximo",
        "calendar.month.1":"Janeiro", "calendar.month.2":"Fevereiro", "calendar.month.3":"Março", "calendar.month.4":"Abril", "calendar.month.5":"Maio", "calendar.month.6":"Junho", "calendar.month.7":"Julho", "calendar.month.8":"Agosto", "calendar.month.9":"Setembro", "calendar.month.10":"Outubro", "calendar.month.11":"Novembro", "calendar.month.12":"Dezembro",
        "calendar.weekday.0":"Seg", "calendar.weekday.1":"Ter", "calendar.weekday.2":"Qua", "calendar.weekday.3":"Qui", "calendar.weekday.4":"Sex", "calendar.weekday.5":"Sáb", "calendar.weekday.6":"Dom",
        "game.rank.1.title":"Iniciante", "game.rank.1.description":"Você começou a construir seu histórico.", "game.rank.3.title":"Constante", "game.rank.3.description":"Seu acompanhamento já virou rotina.", "game.rank.5.title":"Organizado", "game.rank.5.description":"Você está mantendo seus registros em dia.", "game.rank.8.title":"Disciplinado", "game.rank.8.description":"Sua constância já faz diferença no histórico.", "game.rank.12.title":"Veterano", "game.rank.12.description":"Você construiu um histórico consistente.", "game.rank.16.title":"Referência", "game.rank.16.description":"Seu perfil demonstra uma longa sequência de acompanhamento.", "game.rank.20.title":"Mestre do acompanhamento", "game.rank.20.description":"Um longo histórico de organização e constância.",
        "game.achievement.primeiro_passo.title":"Primeiro passo", "game.achievement.primeiro_passo.description":"Faça seu primeiro registro no SaúdeApp.", "game.achievement.constancia_7.title":"7 dias de constância", "game.achievement.constancia_7.description":"Use o acompanhamento em 7 dias diferentes.", "game.achievement.constancia_30.title":"30 dias de constância", "game.achievement.constancia_30.description":"Use o acompanhamento em 30 dias diferentes.", "game.achievement.hidratacao_7.title":"Hidratação em dia", "game.achievement.hidratacao_7.description":"Alcance sua meta de água em 7 dias diferentes.", "game.achievement.dez_registros.title":"Diário ativo", "game.achievement.dez_registros.description":"Faça 10 registros de acompanhamento.", "game.achievement.perfil.title":"Perfil completo", "game.achievement.perfil.description":"Mantenha os dados básicos do perfil preenchidos.",
        "game.mission.acompanhamento.title":"Atualize seu acompanhamento", "game.mission.acompanhamento.description":"Faça pelo menos 1 registro de saúde hoje.", "game.mission.hidratacao.title":"Registre sua hidratação", "game.mission.hidratacao.description":"Adicione pelo menos um registro de água hoje.", "game.mission.organizacao.title":"Mantenha seus registros organizados", "game.mission.organizacao.description":"Registre uma consulta, exame, receita ou agendamento.",
        "game.weekly_mission.semana_acompanhamento.title":"Semana consistente", "game.weekly_mission.semana_acompanhamento.description":"Registre seu acompanhamento em 3 dias diferentes nesta semana.", "game.weekly_mission.semana_hidratacao.title":"Rotina de hidratação", "game.weekly_mission.semana_hidratacao.description":"Faça 5 registros de água durante a semana.", "game.weekly_mission.semana_organizacao.title":"Semana organizada", "game.weekly_mission.semana_organizacao.description":"Registre 2 consultas, exames, receitas ou agendamentos.",
        "game.skill.registro.title":"Registro", "game.skill.registro.description":"Peso, pressão e glicemia", "game.skill.agua.title":"Hidratação", "game.skill.agua.description":"Acompanhamento de água", "game.skill.organizacao.title":"Organização", "game.skill.organizacao.description":"Consultas, exames e receitas", "game.skill.constancia.title":"Constância", "game.skill.constancia.description":"Dias diferentes com atividade",
        "game.reward.2.title":"Título: Constante", "game.reward.2.description":"Desbloqueado ao alcançar o nível 2.", "game.reward.3.title":"Título: Organizado", "game.reward.3.description":"Desbloqueado ao alcançar o nível 3.", "game.reward.5.title":"Título: Disciplinado", "game.reward.5.description":"Desbloqueado ao alcançar o nível 5.", "game.reward.7.title":"Tema de perfil: Safira", "game.reward.7.description":"Desbloqueado ao alcançar o nível 7.", "game.reward.10.title":"Título: Veterano", "game.reward.10.description":"Desbloqueado ao alcançar o nível 10.", "game.reward.15.title":"Tema de perfil: Grafite", "game.reward.15.description":"Desbloqueado ao alcançar o nível 15.",
        "game.activity.perfil_completo":"Perfil básico preenchido", "game.activity.registro_peso":"Registro de peso", "game.activity.registro_pressao":"Registro de pressão", "game.activity.registro_glicemia":"Registro de glicemia", "game.activity.agua_adicao":"Registro de hidratação", "game.activity.meta_agua":"Meta diária de hidratação alcançada", "game.activity.consulta":"Consulta registrada", "game.activity.receita":"Receita registrada", "game.activity.exame":"Exame registrado", "game.activity.agendamento":"Consulta agendada",
        "notifications.pressure_title":"Atenção no acompanhamento", "notifications.pressure_message":"⚠️ Pressão arterial elevada: {value}", "notifications.glucose_title":"Atenção no acompanhamento", "notifications.glucose_message":"🩸 Glicemia elevada: {value}", "notifications.hydration_title":"Atenção no acompanhamento", "notifications.hydration_message":"💧 Você atingiu apenas {value}% da meta de hidratação.", "notifications.bmi_title":"Atenção no acompanhamento", "notifications.bmi_message":"⚖️ IMC de {value} indica obesidade. Consulte um médico.", "notifications.appointment_title":"Consulta próxima", "notifications.appointment_message":"{specialty} com {doctor} em {date} às {time}.",
    },
    "en": {
        "settings.eyebrow":"SYSTEM", "settings.title":"Settings", "settings.subtitle":"Manage your account, privacy and preferences.", "settings.account":"Account", "settings.account_hint":"Access security", "settings.current_password":"Current password", "settings.new_password":"New password", "settings.change_password":"Change password", "settings.preferences":"Preferences", "settings.preferences_hint":"Language and appearance", "settings.language":"Language", "settings.language_hint":"Change it using the selector at the bottom of the interface.", "settings.theme":"Theme", "settings.theme_hint":"Choose between light and dark.", "settings.data":"Your data", "settings.data_hint":"Portability", "settings.data_text":"Download a copy of your records in an open format to keep or analyze.", "settings.export":"Export my data", "settings.export_pdf":"Download report as PDF", "settings.danger":"Danger zone", "settings.danger_hint":"Irreversible operations", "settings.danger_text":"Deleting the account removes your records from the local database.", "settings.delete":"Delete my account", "settings.delete_confirm":"Are you sure? This action cannot be undone.",
        "notifications.eyebrow":"CENTER", "notifications.title":"Notifications", "notifications.subtitle":"Important alerts and reminders for your tracking.", "notifications.mark_all":"Mark all as read", "notifications.mark_read":"Mark as read", "notifications.empty_title":"All caught up.", "notifications.empty_text":"There are no notifications right now.",
        "calendar.eyebrow":"SCHEDULE", "calendar.title":"Calendar", "calendar.subtitle":"View your upcoming appointments in one place.", "calendar.previous":"Previous", "calendar.today":"Today", "calendar.next":"Next", "calendar.month.1":"January", "calendar.month.2":"February", "calendar.month.3":"March", "calendar.month.4":"April", "calendar.month.5":"May", "calendar.month.6":"June", "calendar.month.7":"July", "calendar.month.8":"August", "calendar.month.9":"September", "calendar.month.10":"October", "calendar.month.11":"November", "calendar.month.12":"December", "calendar.weekday.0":"Mon", "calendar.weekday.1":"Tue", "calendar.weekday.2":"Wed", "calendar.weekday.3":"Thu", "calendar.weekday.4":"Fri", "calendar.weekday.5":"Sat", "calendar.weekday.6":"Sun",
        "game.rank.1.title":"Beginner", "game.rank.1.description":"You started building your history.", "game.rank.3.title":"Consistent", "game.rank.3.description":"Your tracking is becoming a routine.", "game.rank.5.title":"Organized", "game.rank.5.description":"You are keeping your records up to date.", "game.rank.8.title":"Disciplined", "game.rank.8.description":"Your consistency is strengthening your history.", "game.rank.12.title":"Veteran", "game.rank.12.description":"You have built a consistent history.", "game.rank.16.title":"Reference", "game.rank.16.description":"Your profile shows a long tracking history.", "game.rank.20.title":"Tracking Master", "game.rank.20.description":"A long history of organization and consistency.",
        "game.achievement.primeiro_passo.title":"First step", "game.achievement.primeiro_passo.description":"Make your first entry in SaúdeApp.", "game.achievement.constancia_7.title":"7 days consistent", "game.achievement.constancia_7.description":"Use tracking on 7 different days.", "game.achievement.constancia_30.title":"30 days consistent", "game.achievement.constancia_30.description":"Use tracking on 30 different days.", "game.achievement.hidratacao_7.title":"Hydration on track", "game.achievement.hidratacao_7.description":"Reach your water goal on 7 different days.", "game.achievement.dez_registros.title":"Active journal", "game.achievement.dez_registros.description":"Make 10 tracking entries.", "game.achievement.perfil.title":"Complete profile", "game.achievement.perfil.description":"Keep your basic profile data filled in.",
        "game.mission.acompanhamento.title":"Update your tracking", "game.mission.acompanhamento.description":"Make at least 1 health entry today.", "game.mission.hidratacao.title":"Log your hydration", "game.mission.hidratacao.description":"Add at least one water entry today.", "game.mission.organizacao.title":"Keep your records organized", "game.mission.organizacao.description":"Record an appointment, exam, prescription or booking.", "game.weekly_mission.semana_acompanhamento.title":"Consistent week", "game.weekly_mission.semana_acompanhamento.description":"Track your health on 3 different days this week.", "game.weekly_mission.semana_hidratacao.title":"Hydration routine", "game.weekly_mission.semana_hidratacao.description":"Log water 5 times during the week.", "game.weekly_mission.semana_organizacao.title":"Organized week", "game.weekly_mission.semana_organizacao.description":"Record 2 appointments, exams, prescriptions or bookings.",
        "game.skill.registro.title":"Tracking", "game.skill.registro.description":"Weight, blood pressure and glucose", "game.skill.agua.title":"Hydration", "game.skill.agua.description":"Water tracking", "game.skill.organizacao.title":"Organization", "game.skill.organizacao.description":"Appointments, exams and prescriptions", "game.skill.constancia.title":"Consistency", "game.skill.constancia.description":"Different days with activity",
        "game.reward.2.title":"Title: Consistent", "game.reward.2.description":"Unlocked at level 2.", "game.reward.3.title":"Title: Organized", "game.reward.3.description":"Unlocked at level 3.", "game.reward.5.title":"Title: Disciplined", "game.reward.5.description":"Unlocked at level 5.", "game.reward.7.title":"Profile theme: Sapphire", "game.reward.7.description":"Unlocked at level 7.", "game.reward.10.title":"Title: Veteran", "game.reward.10.description":"Unlocked at level 10.", "game.reward.15.title":"Profile theme: Graphite", "game.reward.15.description":"Unlocked at level 15.",
        "game.activity.perfil_completo":"Basic profile completed", "game.activity.registro_peso":"Weight entry", "game.activity.registro_pressao":"Blood pressure entry", "game.activity.registro_glicemia":"Glucose entry", "game.activity.agua_adicao":"Hydration entry", "game.activity.meta_agua":"Daily hydration goal reached", "game.activity.consulta":"Appointment recorded", "game.activity.receita":"Prescription recorded", "game.activity.exame":"Exam recorded", "game.activity.agendamento":"Appointment scheduled",
        "notifications.pressure_title":"Tracking alert", "notifications.pressure_message":"⚠️ Elevated blood pressure: {value}", "notifications.glucose_title":"Tracking alert", "notifications.glucose_message":"🩸 Elevated glucose: {value}", "notifications.hydration_title":"Tracking alert", "notifications.hydration_message":"💧 You have reached only {value}% of your hydration goal.", "notifications.bmi_title":"Tracking alert", "notifications.bmi_message":"⚖️ A BMI of {value} indicates obesity. Please consult a doctor.", "notifications.appointment_title":"Upcoming appointment", "notifications.appointment_message":"{specialty} with {doctor} on {date} at {time}.",
    },
    "es": {
        "settings.eyebrow":"SISTEMA", "settings.title":"Configuración", "settings.subtitle":"Controla tu cuenta, privacidad y preferencias.", "settings.account":"Cuenta", "settings.account_hint":"Seguridad de acceso", "settings.current_password":"Contraseña actual", "settings.new_password":"Nueva contraseña", "settings.change_password":"Cambiar contraseña", "settings.preferences":"Preferencias", "settings.preferences_hint":"Idioma y apariencia", "settings.language":"Idioma", "settings.language_hint":"Cámbialo con el selector en la parte inferior de la interfaz.", "settings.theme":"Tema", "settings.theme_hint":"Elige entre claro y oscuro.", "settings.data":"Tus datos", "settings.data_hint":"Portabilidad", "settings.data_text":"Descarga una copia de tus registros en un formato abierto para guardar o analizar.", "settings.export":"Exportar mis datos", "settings.export_pdf":"Descargar informe en PDF", "settings.danger":"Zona de riesgo", "settings.danger_hint":"Operaciones irreversibles", "settings.danger_text":"Eliminar la cuenta borra tus registros de la base de datos local.", "settings.delete":"Eliminar mi cuenta", "settings.delete_confirm":"¿Estás seguro? Esta acción no se puede deshacer.",
        "notifications.eyebrow":"CENTRAL", "notifications.title":"Notificaciones", "notifications.subtitle":"Alertas y recordatorios importantes de tu seguimiento.", "notifications.mark_all":"Marcar todas como leídas", "notifications.mark_read":"Marcar como leída", "notifications.empty_title":"Todo al día.", "notifications.empty_text":"No hay notificaciones en este momento.",
        "calendar.eyebrow":"AGENDA", "calendar.title":"Calendario", "calendar.subtitle":"Visualiza tus próximas citas en un solo lugar.", "calendar.previous":"Anterior", "calendar.today":"Hoy", "calendar.next":"Siguiente", "calendar.month.1":"Enero", "calendar.month.2":"Febrero", "calendar.month.3":"Marzo", "calendar.month.4":"Abril", "calendar.month.5":"Mayo", "calendar.month.6":"Junio", "calendar.month.7":"Julio", "calendar.month.8":"Agosto", "calendar.month.9":"Septiembre", "calendar.month.10":"Octubre", "calendar.month.11":"Noviembre", "calendar.month.12":"Diciembre", "calendar.weekday.0":"Lun", "calendar.weekday.1":"Mar", "calendar.weekday.2":"Mié", "calendar.weekday.3":"Jue", "calendar.weekday.4":"Vie", "calendar.weekday.5":"Sáb", "calendar.weekday.6":"Dom",
        "game.rank.1.title":"Principiante", "game.rank.1.description":"Has comenzado a construir tu historial.", "game.rank.3.title":"Constante", "game.rank.3.description":"Tu seguimiento ya se está convirtiendo en rutina.", "game.rank.5.title":"Organizado", "game.rank.5.description":"Mantienes tus registros al día.", "game.rank.8.title":"Disciplinado", "game.rank.8.description":"Tu constancia fortalece tu historial.", "game.rank.12.title":"Veterano", "game.rank.12.description":"Has construido un historial consistente.", "game.rank.16.title":"Referencia", "game.rank.16.description":"Tu perfil muestra un largo historial de seguimiento.", "game.rank.20.title":"Maestro del seguimiento", "game.rank.20.description":"Un largo historial de organización y constancia.",
        "game.achievement.primeiro_passo.title":"Primer paso", "game.achievement.primeiro_passo.description":"Haz tu primer registro en SaúdeApp.", "game.achievement.constancia_7.title":"7 días de constancia", "game.achievement.constancia_7.description":"Usa el seguimiento en 7 días diferentes.", "game.achievement.constancia_30.title":"30 días de constancia", "game.achievement.constancia_30.description":"Usa el seguimiento en 30 días diferentes.", "game.achievement.hidratacao_7.title":"Hidratación al día", "game.achievement.hidratacao_7.description":"Alcanza tu meta de agua en 7 días diferentes.", "game.achievement.dez_registros.title":"Diario activo", "game.achievement.dez_registros.description":"Haz 10 registros de seguimiento.", "game.achievement.perfil.title":"Perfil completo", "game.achievement.perfil.description":"Mantén completos los datos básicos de tu perfil.",
        "game.mission.acompanhamento.title":"Actualiza tu seguimiento", "game.mission.acompanhamento.description":"Haz al menos 1 registro de salud hoy.", "game.mission.hidratacao.title":"Registra tu hidratación", "game.mission.hidratacao.description":"Añade al menos un registro de agua hoy.", "game.mission.organizacao.title":"Mantén tus registros organizados", "game.mission.organizacao.description":"Registra una cita, examen, receta o reserva.", "game.weekly_mission.semana_acompanhamento.title":"Semana constante", "game.weekly_mission.semana_acompanhamento.description":"Registra tu seguimiento en 3 días diferentes esta semana.", "game.weekly_mission.semana_hidratacao.title":"Rutina de hidratación", "game.weekly_mission.semana_hidratacao.description":"Registra agua 5 veces durante la semana.", "game.weekly_mission.semana_organizacao.title":"Semana organizada", "game.weekly_mission.semana_organizacao.description":"Registra 2 citas, exámenes, recetas o reservas.",
        "game.skill.registro.title":"Registros", "game.skill.registro.description":"Peso, presión y glucosa", "game.skill.agua.title":"Hidratación", "game.skill.agua.description":"Seguimiento del agua", "game.skill.organizacao.title":"Organización", "game.skill.organizacao.description":"Citas, exámenes y recetas", "game.skill.constancia.title":"Constancia", "game.skill.constancia.description":"Días diferentes con actividad",
        "game.reward.2.title":"Título: Constante", "game.reward.2.description":"Desbloqueado al alcanzar el nivel 2.", "game.reward.3.title":"Título: Organizado", "game.reward.3.description":"Desbloqueado al alcanzar el nivel 3.", "game.reward.5.title":"Título: Disciplinado", "game.reward.5.description":"Desbloqueado al alcanzar el nivel 5.", "game.reward.7.title":"Tema de perfil: Zafiro", "game.reward.7.description":"Desbloqueado al alcanzar el nivel 7.", "game.reward.10.title":"Título: Veterano", "game.reward.10.description":"Desbloqueado al alcanzar el nivel 10.", "game.reward.15.title":"Tema de perfil: Grafito", "game.reward.15.description":"Desbloqueado al alcanzar el nivel 15.",
        "game.activity.perfil_completo":"Perfil básico completado", "game.activity.registro_peso":"Registro de peso", "game.activity.registro_pressao":"Registro de presión arterial", "game.activity.registro_glicemia":"Registro de glucosa", "game.activity.agua_adicao":"Registro de hidratación", "game.activity.meta_agua":"Meta diaria de hidratación alcanzada", "game.activity.consulta":"Cita registrada", "game.activity.receita":"Receta registrada", "game.activity.exame":"Examen registrado", "game.activity.agendamento":"Cita programada",
        "notifications.pressure_title":"Alerta de seguimiento", "notifications.pressure_message":"⚠️ Presión arterial elevada: {value}", "notifications.glucose_title":"Alerta de seguimiento", "notifications.glucose_message":"🩸 Glucosa elevada: {value}", "notifications.hydration_title":"Alerta de seguimiento", "notifications.hydration_message":"💧 Solo has alcanzado el {value}% de tu meta de hidratación.", "notifications.bmi_title":"Alerta de seguimiento", "notifications.bmi_message":"⚖️ Un IMC de {value} indica obesidad. Consulta a un médico.", "notifications.appointment_title":"Próxima cita", "notifications.appointment_message":"{specialty} con {doctor} el {date} a las {time}.",
    },
}
for _lang, _values in _EXTRA_TRANSLATIONS.items():
    TRANSLATIONS[_lang].update(_values)


def notification_localized(notification):
    """Converte notificações antigas, salvas em português, para o idioma atual."""
    raw = notification.get("mensagem", "") if hasattr(notification, "get") else ""
    chave = notification.get("chave", "") if hasattr(notification, "get") else ""
    import re
    if "Pressão arterial elevada:" in raw:
        m = re.search(r"(\d+(?:\.\d+)?/\d+(?:\.\d+)?\s*mmHg)", raw)
        value = m.group(1) if m else raw.split(":",1)[-1].strip()
        return {"title": translate("notifications.pressure_title"), "message": translate("notifications.pressure_message", "").format(value=value)}
    if "Glicemia elevada:" in raw:
        m = re.search(r"(\d+(?:\.\d+)?\s*mg/dL)", raw)
        value = m.group(1) if m else raw.split(":",1)[-1].strip()
        return {"title": translate("notifications.glucose_title"), "message": translate("notifications.glucose_message", "").format(value=value)}
    if "Você atingiu apenas" in raw:
        m = re.search(r"([\d.,]+)%", raw)
        value = m.group(1) if m else ""
        return {"title": translate("notifications.hydration_title"), "message": translate("notifications.hydration_message", "").format(value=value)}
    if "IMC de" in raw and "obesidade" in raw.lower():
        m = re.search(r"IMC de\s+([\d.,]+)", raw)
        value = m.group(1) if m else ""
        return {"title": translate("notifications.bmi_title"), "message": translate("notifications.bmi_message", "").format(value=value)}
    if chave.startswith("agendamento:"):
        m = re.search(r"^(.*?) com (.*?) em (\d{4}-\d{2}-\d{2}) às (\d{2}:\d{2})\.?$", raw)
        if m:
            return {"title": translate("notifications.appointment_title"), "message": translate("notifications.appointment_message", "").format(specialty=m.group(1), doctor=m.group(2), date=m.group(3), time=m.group(4))}
    return {"title": notification.get("titulo", ""), "message": raw}

TRANSLATIONS["pt-BR"].update({
    "common.doctor_prefix":"Dr(a).", "common.remove_confirm":"Remover esta consulta?"
})
TRANSLATIONS["en"].update({
    "common.doctor_prefix":"Dr.", "common.remove_confirm":"Remove this visit?"
})
TRANSLATIONS["es"].update({
    "common.doctor_prefix":"Dr(a).", "common.remove_confirm":"¿Eliminar esta consulta?"
})

TRANSLATIONS["pt-BR"].update({
    "common.user_not_found":"Usuário não encontrado.",
    "consultations.invalid_fields":"Informe médico e especialidade.",
    "consultations.invalid_date":"Data da consulta inválida.",
    "consultations.added_success":"Consulta adicionada com sucesso.",
    "consultations.not_found":"Consulta não encontrada.",
    "consultations.removed_success":"Consulta removida."
})
TRANSLATIONS["en"].update({
    "common.user_not_found":"User not found.",
    "consultations.invalid_fields":"Enter the doctor and specialty.",
    "consultations.invalid_date":"Invalid visit date.",
    "consultations.added_success":"Visit added successfully.",
    "consultations.not_found":"Visit not found.",
    "consultations.removed_success":"Visit removed."
})
TRANSLATIONS["es"].update({
    "common.user_not_found":"Usuario no encontrado.",
    "consultations.invalid_fields":"Informa el médico y la especialidad.",
    "consultations.invalid_date":"Fecha de consulta no válida.",
    "consultations.added_success":"Consulta añadida correctamente.",
    "consultations.not_found":"Consulta no encontrada.",
    "consultations.removed_success":"Consulta eliminada."
})

TRANSLATIONS["pt-BR"].update({"auth.invalid_login":"Login ou senha incorretos.","record.updated":"Prontuário atualizado!","profile.photo_invalid":"A foto deve ser JPG, JPEG, PNG ou WEBP.","profile.account_deleted":"Conta excluída.","docs.prescription_not_found":"Receita não encontrada.","docs.appointment_not_found":"Agendamento não encontrado.","docs.exam_not_found":"Exame não encontrado."})
TRANSLATIONS["en"].update({"auth.invalid_login":"Incorrect username or password.","record.updated":"Medical record updated!","profile.photo_invalid":"The photo must be JPG, JPEG, PNG or WEBP.","profile.account_deleted":"Account deleted.","docs.prescription_not_found":"Prescription not found.","docs.appointment_not_found":"Appointment not found.","docs.exam_not_found":"Exam not found."})
TRANSLATIONS["es"].update({"auth.invalid_login":"Usuario o contraseña incorrectos.","record.updated":"¡Historial médico actualizado!","profile.photo_invalid":"La foto debe ser JPG, JPEG, PNG o WEBP.","profile.account_deleted":"Cuenta eliminada.","docs.prescription_not_found":"Receta no encontrada.","docs.appointment_not_found":"Cita no encontrada.","docs.exam_not_found":"Examen no encontrado."})

LANG_NAMES = {"pt-BR": "Português", "en": "English", "es": "Español"}

def normalize_language(value):
    return value if value in TRANSLATIONS else "pt-BR"

def get_language():
    return normalize_language(session.get("idioma", "pt-BR"))

def translate(key, default=None):
    lang = get_language()
    return TRANSLATIONS.get(lang, {}).get(key) or TRANSLATIONS["pt-BR"].get(key) or default or key

def language_names():
    return LANG_NAMES

# Auditoria 3.8: chaves que eram usadas pelos templates mas ainda não estavam
# cadastradas em todos os idiomas. Mantemos as chaves centralizadas aqui para
# evitar que identificadores internos apareçam na interface.
TRANSLATIONS["pt-BR"].update({
    "auth.home":"Voltar à página inicial",
    "base.navigation":"Navegação principal", "base.academic":"Projeto acadêmico", "base.local":"Dados locais",
    "ai.brand":"ASSISTENTE IA", "ai.next_prompt":"Quais são minhas próximas consultas?", "ai.summary_prompt":"Faça um resumo dos meus registros recentes.", "ai.response":"Resposta", "ai.configuration":"Configuração necessária",
    "appointments.complete_title":"Concluir consulta", "appointments.completed":"Realizada", "appointments.diagnosis_example":"Ex.: acompanhamento de rotina", "appointments.doctor_prefix":"Dr(a).", "appointments.location_example":"Ex.: Clínica Central, sala 4",
    "docs.prescriptions":"Receitas", "docs.prescription_for":"Receita de", "docs.medication_count":"medicamento(s)", "docs.exams":"Exames", "docs.appointments":"Agendamentos", "docs.appointment_at":"às",
    "exams.date":"Data", "exams.file_header":"Arquivo", "exams.notes_header":"Observações", "exams.remove_confirm":"Remover este exame?", "exams.result_example":"Ex.: resultado principal", "exams.result_header":"Resultado", "exams.type_example":"Ex.: Hemograma",
    "prescriptions.doctor_prefix":"Dr(a).", "prescriptions.name_placeholder":"Nome do medicamento", "prescriptions.dose_placeholder":"Dosagem", "prescriptions.frequency_placeholder":"Frequência", "prescriptions.duration_placeholder":"Duração", "prescriptions.remove_confirm":"Remover esta receita?",
    "profile.confirm_delete":"Tem certeza? Esta ação é irreversível.",
    "record.allergies_example":"Ex.: penicilina, dipirona", "record.allergies_label":"Alergias:", "record.chronic_example":"Ex.: asma, hipertensão", "record.chronic_label":"Doenças crônicas:", "record.continuous_example":"Ex.: medicamento de uso contínuo", "record.continuous_label":"Medicamentos de uso contínuo:",
    "register.name_example":"Ex.: Maria da Silva", "register.point_records":"Seus registros ficam organizados", "register.point_routine":"Acompanhe sua rotina ao longo do tempo", "register.point_progress":"Desbloqueie progresso conforme participa",
})
TRANSLATIONS["en"].update({
    "auth.home":"Back to home",
    "base.navigation":"Main navigation", "base.academic":"Academic project", "base.local":"Local data",
    "ai.brand":"AI ASSISTANT", "ai.next_prompt":"What are my next appointments?", "ai.summary_prompt":"Give me a summary of my recent records.", "ai.response":"Response", "ai.configuration":"Configuration required",
    "appointments.complete_title":"Complete appointment", "appointments.completed":"Completed", "appointments.diagnosis_example":"Example: routine follow-up", "appointments.doctor_prefix":"Dr.", "appointments.location_example":"Example: Central Clinic, room 4",
    "docs.prescriptions":"Prescriptions", "docs.prescription_for":"Prescription for", "docs.medication_count":"medication(s)", "docs.exams":"Exams", "docs.appointments":"Appointments", "docs.appointment_at":"at",
    "exams.date":"Date", "exams.file_header":"File", "exams.notes_header":"Notes", "exams.remove_confirm":"Remove this exam?", "exams.result_example":"Example: main result", "exams.result_header":"Result", "exams.type_example":"Example: Complete blood count",
    "prescriptions.doctor_prefix":"Dr.", "prescriptions.name_placeholder":"Medication name", "prescriptions.dose_placeholder":"Dosage", "prescriptions.frequency_placeholder":"Frequency", "prescriptions.duration_placeholder":"Duration", "prescriptions.remove_confirm":"Remove this prescription?",
    "profile.confirm_delete":"Are you sure? This action cannot be undone.",
    "record.allergies_example":"Example: penicillin, dipyrone", "record.allergies_label":"Allergies:", "record.chronic_example":"Example: asthma, hypertension", "record.chronic_label":"Chronic conditions:", "record.continuous_example":"Example: continuous medication", "record.continuous_label":"Continuous medications:",
    "register.name_example":"Example: Maria Silva", "register.point_records":"Keep your records organized", "register.point_routine":"Follow your routine over time", "register.point_progress":"Unlock progress as you participate",
})
TRANSLATIONS["es"].update({
    "auth.home":"Volver al inicio",
    "base.navigation":"Navegación principal", "base.academic":"Proyecto académico", "base.local":"Datos locales",
    "ai.brand":"ASISTENTE IA", "ai.next_prompt":"¿Cuáles son mis próximas citas?", "ai.summary_prompt":"Haz un resumen de mis registros recientes.", "ai.response":"Respuesta", "ai.configuration":"Configuración necesaria",
    "appointments.complete_title":"Completar cita", "appointments.completed":"Realizada", "appointments.diagnosis_example":"Ej.: seguimiento de rutina", "appointments.doctor_prefix":"Dr(a).", "appointments.location_example":"Ej.: Clínica Central, sala 4",
    "docs.prescriptions":"Recetas", "docs.prescription_for":"Receta de", "docs.medication_count":"medicamento(s)", "docs.exams":"Exámenes", "docs.appointments":"Citas", "docs.appointment_at":"a las",
    "exams.date":"Fecha", "exams.file_header":"Archivo", "exams.notes_header":"Observaciones", "exams.remove_confirm":"¿Eliminar este examen?", "exams.result_example":"Ej.: resultado principal", "exams.result_header":"Resultado", "exams.type_example":"Ej.: Hemograma",
    "prescriptions.doctor_prefix":"Dr(a).", "prescriptions.name_placeholder":"Nombre del medicamento", "prescriptions.dose_placeholder":"Dosis", "prescriptions.frequency_placeholder":"Frecuencia", "prescriptions.duration_placeholder":"Duración", "prescriptions.remove_confirm":"¿Eliminar esta receta?",
    "profile.confirm_delete":"¿Estás seguro? Esta acción es irreversible.",
    "record.allergies_example":"Ej.: penicilina, dipirona", "record.allergies_label":"Alergias:", "record.chronic_example":"Ej.: asma, hipertensión", "record.chronic_label":"Enfermedades crónicas:", "record.continuous_example":"Ej.: medicamento de uso continuo", "record.continuous_label":"Medicamentos de uso continuo:",
    "register.name_example":"Ej.: María Silva", "register.point_records":"Mantén tus registros organizados", "register.point_routine":"Acompaña tu rutina con el tiempo", "register.point_progress":"Desbloquea progreso al participar",
})

# Auditoria final: mensagens do backend, validações e erros também usam i18n.
TRANSLATIONS["pt-BR"].update({
    "auth.login_exists":"Este login já está cadastrado.",
    "register.success":"Cadastro realizado!", "register.invalid_numbers":"Preencha idade, altura, peso e meta de água com valores válidos.", "register.invalid_age":"A idade deve estar entre 0 e 120 anos.", "register.invalid_height":"A altura deve estar entre 0,50 m e 2,50 m.", "register.invalid_weight":"O peso deve estar entre 1 e 500 kg.", "register.invalid_water":"A meta de água deve estar entre 0,5 e 10 litros.",
    "profile.updated":"Perfil atualizado com sucesso.", "profile.invalid_numbers":"Idade, altura, peso e meta de água devem ser numéricos.", "profile.invalid_height":"A altura deve estar entre 0,50 e 2,50 m.", "profile.invalid_water":"A meta de água deve estar entre 0,5 e 10 L.",
    "settings.current_password_invalid":"A senha atual está incorreta.", "settings.password_short":"A nova senha deve ter pelo menos 8 caracteres.", "settings.password_changed":"Senha alterada com sucesso.",
    "dash.water_invalid":"Informe uma quantidade de água válida.", "dash.water_positive":"A quantidade de água deve ser maior que zero.", "dash.water_max_add":"Não é permitido adicionar mais de 2 litros de uma vez.", "dash.water_daily_limit":"O registro ultrapassaria 10 litros de água no dia.", "dash.weight_invalid":"Informe um peso válido.", "dash.weight_saved":"Peso registrado com sucesso.",
    "dash.pressure_invalid":"Informe valores numéricos para a pressão.", "dash.systolic_range":"A pressão sistólica deve estar entre 50 e 300 mmHg.", "dash.diastolic_range":"A pressão diastólica deve estar entre 30 e 200 mmHg.", "dash.diastolic_less":"A pressão diastólica deve ser menor que a sistólica.", "dash.pressure_saved":"Pressão registrada com sucesso.",
    "dash.glucose_invalid":"Informe um valor de glicemia válido.", "dash.glucose_range":"O valor informado está fora da faixa plausível do sistema (20 a 1000 mg/dL).", "dash.glucose_saved":"Glicemia registrada com sucesso.",
    "prescriptions.doctor_required":"Informe o nome do profissional.", "prescriptions.medication_required":"Adicione pelo menos um medicamento.", "prescriptions.medication_limit":"Limite de 20 medicamentos por receita.", "prescriptions.added_success":"Receita adicionada com sucesso.", "prescriptions.not_found":"Receita não encontrada.", "prescriptions.removed_success":"Receita removida.",
    "exams.type_required":"Informe o tipo do exame.", "exams.type_too_long":"O tipo do exame é muito longo.", "exams.added_success":"Exame registrado com sucesso.", "exams.not_found":"Exame não encontrado.", "exams.removed_success":"Exame removido.",
    "appointments.datetime_invalid":"Informe uma data e horário válidos.", "appointments.future_server":"O agendamento precisa ser para o futuro.", "appointments.duplicate":"Já existe um agendamento para esse horário.", "appointments.added_success":"Consulta agendada com sucesso.", "appointments.not_found":"Agendamento não encontrado.", "appointments.cannot_cancel":"Esse agendamento não pode mais ser cancelado.", "appointments.cancelled":"Agendamento cancelado.", "appointments.already_completed":"Esse agendamento já foi encerrado.", "appointments.completed_success":"Consulta concluída e adicionada ao prontuário.",
    "docs.document_not_found":"Documento não encontrado.",
    "errors.not_found":"A página solicitada não existe.", "errors.file_too_large":"O arquivo enviado ultrapassa o limite de 16 MB.", "errors.internal":"O sistema encontrou um erro interno. Tente novamente.",
})
TRANSLATIONS["en"].update({
    "auth.login_exists":"This login is already registered.",
    "register.success":"Registration completed!", "register.invalid_numbers":"Enter valid values for age, height, weight, and daily water goal.", "register.invalid_age":"Age must be between 0 and 120 years.", "register.invalid_height":"Height must be between 0.50 m and 2.50 m.", "register.invalid_weight":"Weight must be between 1 and 500 kg.", "register.invalid_water":"The water goal must be between 0.5 and 10 liters.",
    "profile.updated":"Profile updated successfully.", "profile.invalid_numbers":"Age, height, weight, and water goal must be numeric.", "profile.invalid_height":"Height must be between 0.50 and 2.50 m.", "profile.invalid_water":"The water goal must be between 0.5 and 10 L.",
    "settings.current_password_invalid":"The current password is incorrect.", "settings.password_short":"The new password must be at least 8 characters long.", "settings.password_changed":"Password changed successfully.",
    "dash.water_invalid":"Enter a valid amount of water.", "dash.water_positive":"The amount of water must be greater than zero.", "dash.water_max_add":"You cannot add more than 2 liters at once.", "dash.water_daily_limit":"This entry would exceed 10 liters of water for the day.", "dash.weight_invalid":"Enter a valid weight.", "dash.weight_saved":"Weight recorded successfully.",
    "dash.pressure_invalid":"Enter numeric blood pressure values.", "dash.systolic_range":"Systolic pressure must be between 50 and 300 mmHg.", "dash.diastolic_range":"Diastolic pressure must be between 30 and 200 mmHg.", "dash.diastolic_less":"Diastolic pressure must be lower than systolic pressure.", "dash.pressure_saved":"Blood pressure recorded successfully.",
    "dash.glucose_invalid":"Enter a valid glucose value.", "dash.glucose_range":"The value is outside the system's plausible range (20 to 1000 mg/dL).", "dash.glucose_saved":"Glucose recorded successfully.",
    "prescriptions.doctor_required":"Enter the professional's name.", "prescriptions.medication_required":"Add at least one medication.", "prescriptions.medication_limit":"A prescription can contain up to 20 medications.", "prescriptions.added_success":"Prescription added successfully.", "prescriptions.not_found":"Prescription not found.", "prescriptions.removed_success":"Prescription removed.",
    "exams.type_required":"Enter the exam type.", "exams.type_too_long":"The exam type is too long.", "exams.added_success":"Exam recorded successfully.", "exams.not_found":"Exam not found.", "exams.removed_success":"Exam removed.",
    "appointments.datetime_invalid":"Enter a valid date and time.", "appointments.future_server":"The appointment must be scheduled for the future.", "appointments.duplicate":"There is already an appointment at that time.", "appointments.added_success":"Appointment scheduled successfully.", "appointments.not_found":"Appointment not found.", "appointments.cannot_cancel":"This appointment can no longer be cancelled.", "appointments.cancelled":"Appointment cancelled.", "appointments.already_completed":"This appointment has already been completed.", "appointments.completed_success":"Appointment completed and added to the medical record.",
    "docs.document_not_found":"Document not found.",
    "errors.not_found":"The requested page does not exist.", "errors.file_too_large":"The uploaded file exceeds the 16 MB limit.", "errors.internal":"The system encountered an internal error. Please try again.",
})
TRANSLATIONS["es"].update({
    "auth.login_exists":"Este usuario ya está registrado.",
    "register.success":"¡Registro realizado!", "register.invalid_numbers":"Completa edad, altura, peso y meta de agua con valores válidos.", "register.invalid_age":"La edad debe estar entre 0 y 120 años.", "register.invalid_height":"La altura debe estar entre 0,50 m y 2,50 m.", "register.invalid_weight":"El peso debe estar entre 1 y 500 kg.", "register.invalid_water":"La meta de agua debe estar entre 0,5 y 10 litros.",
    "profile.updated":"Perfil actualizado correctamente.", "profile.invalid_numbers":"La edad, altura, peso y meta de agua deben ser numéricos.", "profile.invalid_height":"La altura debe estar entre 0,50 y 2,50 m.", "profile.invalid_water":"La meta de agua debe estar entre 0,5 y 10 L.",
    "settings.current_password_invalid":"La contraseña actual es incorrecta.", "settings.password_short":"La nueva contraseña debe tener al menos 8 caracteres.", "settings.password_changed":"Contraseña cambiada correctamente.",
    "dash.water_invalid":"Introduce una cantidad de agua válida.", "dash.water_positive":"La cantidad de agua debe ser mayor que cero.", "dash.water_max_add":"No puedes añadir más de 2 litros de una vez.", "dash.water_daily_limit":"Este registro superaría los 10 litros de agua del día.", "dash.weight_invalid":"Introduce un peso válido.", "dash.weight_saved":"Peso registrado correctamente.",
    "dash.pressure_invalid":"Introduce valores numéricos para la presión arterial.", "dash.systolic_range":"La presión sistólica debe estar entre 50 y 300 mmHg.", "dash.diastolic_range":"La presión diastólica debe estar entre 30 y 200 mmHg.", "dash.diastolic_less":"La presión diastólica debe ser menor que la sistólica.", "dash.pressure_saved":"Presión arterial registrada correctamente.",
    "dash.glucose_invalid":"Introduce un valor de glucosa válido.", "dash.glucose_range":"El valor está fuera del rango plausible del sistema (20 a 1000 mg/dL).", "dash.glucose_saved":"Glucosa registrada correctamente.",
    "prescriptions.doctor_required":"Introduce el nombre del profesional.", "prescriptions.medication_required":"Añade al menos un medicamento.", "prescriptions.medication_limit":"Una receta puede contener hasta 20 medicamentos.", "prescriptions.added_success":"Receta añadida correctamente.", "prescriptions.not_found":"Receta no encontrada.", "prescriptions.removed_success":"Receta eliminada.",
    "exams.type_required":"Introduce el tipo de examen.", "exams.type_too_long":"El tipo de examen es demasiado largo.", "exams.added_success":"Examen registrado correctamente.", "exams.not_found":"Examen no encontrado.", "exams.removed_success":"Examen eliminado.",
    "appointments.datetime_invalid":"Introduce una fecha y hora válidas.", "appointments.future_server":"La cita debe programarse para el futuro.", "appointments.duplicate":"Ya existe una cita para esa hora.", "appointments.added_success":"Cita programada correctamente.", "appointments.not_found":"Cita no encontrada.", "appointments.cannot_cancel":"Esta cita ya no se puede cancelar.", "appointments.cancelled":"Cita cancelada.", "appointments.already_completed":"Esta cita ya se ha completado.", "appointments.completed_success":"Cita completada y añadida al historial médico.",
    "docs.document_not_found":"Documento no encontrado.",
    "errors.not_found":"La página solicitada no existe.", "errors.file_too_large":"El archivo enviado supera el límite de 16 MB.", "errors.internal":"El sistema encontró un error interno. Inténtalo de nuevo.",
})

# Mensagens do assistente e textos dos PDFs também respeitam o idioma atual.
TRANSLATIONS["pt-BR"].update({
    "ai.empty_question":"Digite uma pergunta.", "ai.not_configured":"A IA ainda não está configurada. Defina a variável de ambiente OPENAI_API_KEY para ativar o assistente.", "ai.library_missing":"A biblioteca da IA não está instalada. Execute: pip install -r requirements.txt", "ai.no_response":"A IA não retornou uma resposta.", "ai.request_failed":"Não foi possível consultar a IA agora. Verifique a configuração da API e tente novamente.",
    "docs.simulated_notice":"DOCUMENTO SIMULADO • SEM VALIDADE OFICIAL", "docs.footer":"SaúdeApp • documento para fins acadêmicos/demonstração • sem validade oficial", "docs.demo_code":"Código de demonstração", "docs.qr_instruction":"Escaneie o QR para abrir a página de verificação do registro dentro do SaúdeApp.",
    "docs.health_summary":"Resumo de Saúde", "docs.prescription_demo":"Receita — demonstração", "docs.appointment_demo":"Comprovante de agendamento — demonstração", "docs.exam_demo":"Registro de exame — demonstração", "docs.patient_card":"Cartão de paciente — demonstração", "docs.patient":"Paciente", "docs.generated_at":"Gerado em", "docs.date":"Data", "docs.field":"Campo", "docs.information":"Informação", "docs.age":"Idade", "docs.years":"anos", "docs.blood_type":"Tipo sanguíneo", "docs.not_informed":"Não informado", "docs.height":"Altura", "docs.weight":"Peso", "docs.water_goal":"Meta de água", "docs.day":"dia", "docs.latest_measurements":"Últimas medições", "docs.measurement":"Medição", "docs.value":"Valor", "docs.pressure":"Pressão", "docs.glucose":"Glicemia", "docs.water_today":"Água hoje", "docs.not_recorded":"Não registrada", "docs.professional":"Profissional", "docs.specialty":"Especialidade", "docs.time":"Horário", "docs.location":"Local", "docs.status":"Status", "docs.scheduled":"Agendado", "docs.cancelled":"Cancelado", "docs.completed":"Realizado", "docs.medication":"Medicamento", "docs.dosage":"Dosagem", "docs.frequency":"Frequência", "docs.duration":"Duração", "docs.exam":"Exame", "docs.result":"Resultado", "docs.notes":"Observações", "docs.file":"Arquivo", "docs.no_file":"Nenhum arquivo anexado", "docs.name":"Nome", "docs.identifier":"Identificador", "docs.internal_registration":"Cadastro interno do SaúdeApp",
    "docs.prescription_note":"Observação: esta receita é uma representação visual para demonstração do sistema. Não substitui prescrição emitida por profissional habilitado.", "docs.appointment_note":"Este comprovante é apenas uma simulação gerada pelo SaúdeApp.", "docs.exam_note":"O conteúdo deste documento é fornecido pelo usuário e não representa um laudo laboratorial oficial.", "docs.card_note":"Este cartão é uma identificação interna da aplicação e não substitui documento oficial nem cartão do SUS.",
})
TRANSLATIONS["en"].update({
    "ai.empty_question":"Enter a question.", "ai.not_configured":"The AI is not configured yet. Set the OPENAI_API_KEY environment variable to enable the assistant.", "ai.library_missing":"The AI library is not installed. Run: pip install -r requirements.txt", "ai.no_response":"The AI did not return a response.", "ai.request_failed":"The AI could not be reached right now. Check the API configuration and try again.",
    "docs.simulated_notice":"SIMULATED DOCUMENT • NO OFFICIAL VALIDITY", "docs.footer":"HealthApp • academic/demonstration document • no official validity", "docs.demo_code":"Demonstration code", "docs.qr_instruction":"Scan the QR code to open the record verification page inside SaúdeApp.",
    "docs.health_summary":"Health Summary", "docs.prescription_demo":"Prescription — demonstration", "docs.appointment_demo":"Appointment receipt — demonstration", "docs.exam_demo":"Exam record — demonstration", "docs.patient_card":"Patient card — demonstration", "docs.patient":"Patient", "docs.generated_at":"Generated on", "docs.date":"Date", "docs.field":"Field", "docs.information":"Information", "docs.age":"Age", "docs.years":"years", "docs.blood_type":"Blood type", "docs.not_informed":"Not provided", "docs.height":"Height", "docs.weight":"Weight", "docs.water_goal":"Water goal", "docs.day":"day", "docs.latest_measurements":"Latest measurements", "docs.measurement":"Measurement", "docs.value":"Value", "docs.pressure":"Blood pressure", "docs.glucose":"Glucose", "docs.water_today":"Water today", "docs.not_recorded":"Not recorded", "docs.professional":"Professional", "docs.specialty":"Specialty", "docs.time":"Time", "docs.location":"Location", "docs.status":"Status", "docs.scheduled":"Scheduled", "docs.cancelled":"Cancelled", "docs.completed":"Completed", "docs.medication":"Medication", "docs.dosage":"Dosage", "docs.frequency":"Frequency", "docs.duration":"Duration", "docs.exam":"Exam", "docs.result":"Result", "docs.notes":"Notes", "docs.file":"File", "docs.no_file":"No file attached", "docs.name":"Name", "docs.identifier":"Identifier", "docs.internal_registration":"Internal SaúdeApp registration",
    "docs.prescription_note":"Note: this prescription is a visual representation for system demonstration. It does not replace a prescription issued by a qualified professional.", "docs.appointment_note":"This receipt is only a simulation generated by SaúdeApp.", "docs.exam_note":"The content of this document is provided by the user and does not represent an official laboratory report.", "docs.card_note":"This card is an internal application identification and does not replace an official document or SUS card.",
})
TRANSLATIONS["es"].update({
    "ai.empty_question":"Escribe una pregunta.", "ai.not_configured":"La IA aún no está configurada. Define la variable de entorno OPENAI_API_KEY para activar el asistente.", "ai.library_missing":"La biblioteca de IA no está instalada. Ejecuta: pip install -r requirements.txt", "ai.no_response":"La IA no devolvió una respuesta.", "ai.request_failed":"No fue posible consultar la IA ahora. Comprueba la configuración de la API e inténtalo de nuevo.",
    "docs.simulated_notice":"DOCUMENTO SIMULADO • SIN VALIDEZ OFICIAL", "docs.footer":"SaúdeApp • documento para fines académicos/demostración • sin validez oficial", "docs.demo_code":"Código de demostración", "docs.qr_instruction":"Escanea el QR para abrir la página de verificación del registro dentro de SaúdeApp.",
    "docs.health_summary":"Resumen de salud", "docs.prescription_demo":"Receta — demostración", "docs.appointment_demo":"Comprobante de cita — demostración", "docs.exam_demo":"Registro de examen — demostración", "docs.patient_card":"Tarjeta de paciente — demostración", "docs.patient":"Paciente", "docs.generated_at":"Generado el", "docs.date":"Fecha", "docs.field":"Campo", "docs.information":"Información", "docs.age":"Edad", "docs.years":"años", "docs.blood_type":"Tipo sanguíneo", "docs.not_informed":"No informado", "docs.height":"Altura", "docs.weight":"Peso", "docs.water_goal":"Meta de agua", "docs.day":"día", "docs.latest_measurements":"Últimas mediciones", "docs.measurement":"Medición", "docs.value":"Valor", "docs.pressure":"Presión arterial", "docs.glucose":"Glucosa", "docs.water_today":"Agua de hoy", "docs.not_recorded":"No registrada", "docs.professional":"Profesional", "docs.specialty":"Especialidad", "docs.time":"Hora", "docs.location":"Lugar", "docs.status":"Estado", "docs.scheduled":"Programada", "docs.cancelled":"Cancelada", "docs.completed":"Realizada", "docs.medication":"Medicamento", "docs.dosage":"Dosis", "docs.frequency":"Frecuencia", "docs.duration":"Duración", "docs.exam":"Examen", "docs.result":"Resultado", "docs.notes":"Observaciones", "docs.file":"Archivo", "docs.no_file":"Ningún archivo adjunto", "docs.name":"Nombre", "docs.identifier":"Identificador", "docs.internal_registration":"Registro interno de SaúdeApp",
    "docs.prescription_note":"Observación: esta receta es una representación visual para la demostración del sistema. No sustituye una receta emitida por un profesional habilitado.", "docs.appointment_note":"Este comprobante es solo una simulación generada por SaúdeApp.", "docs.exam_note":"El contenido de este documento lo proporciona el usuario y no representa un informe de laboratorio oficial.", "docs.card_note":"Esta tarjeta es una identificación interna de la aplicación y no sustituye un documento oficial ni la tarjeta del SUS.",
})
