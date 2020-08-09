import settings

name = settings.get_setting("assistant_name")

#Lights
turn_on_light_room = ["accendi la luce in", "accendi luce in", "accendi stanza", "accendi la stanza", "accendi la luce nella stanza"]
turn_off_light_room = ["spegni la luce in", "spegni luce in", "spegni stabza", "spegni la stanza", "spegni la luce nella stanza"]
turn_on_light = ["accendi dispositivo", "accendi il dispositivo"]
turn_on = ["accendi la luce", "accendi luce", "accendi luci"]
turn_off = ["spegni la luce", "spegni luce", "spegni luci"]

#Chat
call_assistant = ["ehi " + name, "ciao " + name, "buongiorno " + name, name, "ok " + name, "buonasera " + name, "buon pomeriggio " + name]
shutdown = ["disattiva il sistema", "spegni il sistema", "spegniti", "vai a dormire", "ritorna nella pokeball"]
hello = ["ciao"]
cancel = ["annulla", "non importa", "no", "scherzavo"]

#Music
play_music = ["riproduci", "metti", "fammi ascoltare", "fammi sentire", "voglio ascoltare", "voglio sentire"]
pause_music = ["metti in pausa", "metti in pausa la musica", "pausa", "pausa musica", "musica in pausa"]
resume_music = ["riprendi", "riprendi musica", "riprendi la musica", "riavvia musica", "riavvia la musica", "continua musica", "continua la musica"]
stop_music = ["interrompi", "interrompi musica", "interrompi la musica", "stop", "stop musica", "stop alla musica", "ferma", "ferma musica", "ferma la musica"]

#Authorization level
auth_levels = {-1 : 'Ospite', 0 : 'Utente generico', 1 : 'Admin', 2 : 'Super utente', 'Ospite' : -1, 'Utente generico' : 0, 'Admin' : 1, 'Super user' : 2}

#Settings management
set_setting = [ "configura le impostazioni", "imposta le impostazioni", "modifica le impostazioni", "cambia le impostazioni", "aggiorna le impostazioni", "configura impostazioni", "imposta impostazioni", "modifica impostazioni", "cambia impostazioni", "aggiorna impostazioni"]
reset_settings = [ "reimposta le impostazioni", "resetta le impostazioni", "ripristina le impostazioni"]
