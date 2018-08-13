from api.models import Employee, ShiftInvite, Shift
from api.utils.email import send_email_message
import api.utils.jwt
import rest_framework_jwt

jwt_encode_handler = rest_framework_jwt.settings.api_settings.JWT_ENCODE_HANDLER;

def get_talents_to_notify(shift):
    
    talents_to_notify = []
    if shift.status == 'OPEN':
        rating = shift.minimum_allowed_rating
        favorite_lists = shift.allowed_from_list.all()
        if len(favorite_lists) == 0:
            talents_to_notify = Employee.objects.filter(
                rating__gte=rating,
                #the employee gets to pick the minimum hourly rate
                minimum_hourly_rate__lte=shift.minimum_hourly_rate
            )
        else:
            talents_to_notify = Employee.objects.filter(
                rating__gte=rating, 
                #the employer gets to pick employers only from his favlists
                favoritelist__in=favorite_lists,
                #the employee gets to pick the minimum hourly rate
                minimum_hourly_rate__lte=shift.minimum_hourly_rate
            )
    
    if shift.status == 'CANCELLED':
        talents_to_notify = shift.candidates.all() | shift.employees.all()
    
    return talents_to_notify

# automatic notification
def shift_update(user, shift, status='being_updated'):
    shift = Shift.objects.get(id=shift.id) #IMPORTANT: override the shift
    talents_to_notify = get_talents_to_notify(shift)
    
    if status == 'being_updated':
        for talent in talents_to_notify:
            payload = api.utils.jwt.jwt_payload_handler({
                "user_id": talent.profile.user.id,
                "shift_id": shift.id
            })
            token = jwt_encode_handler(payload)
            
            ShiftInvite.objects.create(
                sender=user.profile, 
                shift=shift, 
                employee=talent
            )

            send_email_message('new_shift', talent.profile.user.email, {
                "COMPANY": shift.employer.title,
                "POSITION": shift.position.title,
                "TOKEN": token,
                "DATE": shift.date
            })
            
    if status == 'being_cancelled':
        for talent in talents_to_notify:
            send_email_message('deleted_shift', talent.profile.user.email, {
                "COMPANY": shift.employer.title,
                "POSITION": shift.position.title,
                "TOKEN": token,
                "DATE": shift.date
            })

def shift_candidate_update(user, shift, talents_to_notify=[]):
    
    for talent in talents_to_notify['accepted']:
        payload = api.utils.jwt.jwt_payload_handler({
            "user_id": talent.profile.user.id,
            "shift_id": shift.id
        })
        send_email_message('applicant_accepted', talent.profile.user.email, {
            "COMPANY": shift.employer.title,
            "POSITION": shift.position.title,
            "TOKEN": jwt_encode_handler(payload),
            "DATE": shift.date
        })
    
    for talent in talents_to_notify['rejected']:
        payload = api.utils.jwt.jwt_payload_handler({
            "user_id": talent.profile.user.id,
            "shift_id": shift.id
        })
        send_email_message('applicant_rejected', talent.profile.user.email, {
            "COMPANY": shift.employer.title,
            "POSITION": shift.position.title,
            "TOKEN": jwt_encode_handler(payload),
            "DATE": shift.date
        })

# manual invite
def jobcore_invite(invite):
    
    payload = api.utils.jwt.jwt_payload_handler({
        "sender_id": invite.sender.id,
        "invite_id": invite.id
    })
    token = jwt_encode_handler(payload)
        
    send_email_message("invite_to_jobcore", invite.email, {
        "SENDER": invite.sender.user.first_name + ' ' + invite.sender.user.last_name,
        "EMAIL": invite.email,
        "COMPANY": invite.sender.user.profile.employer.title,
        "TOKEN": token
    })

# manual invite
def shift_invite(invite):
    
    payload = api.utils.jwt.jwt_payload_handler({
        "sender_id": invite.sender.id,
        "invite_id": invite.id
    })
    token = jwt_encode_handler(payload)
    
    send_email_message("invite_to_shift", "alejandro@bestmiamiweddings.com", {
        "SENDER": invite.sender.user.first_name + ' ' + invite.sender.user.last_name,
        "COMPANY": invite.sender.user.profile.employer.title,
        "POSITION": invite.shift.position.title,
        "DATE": invite.shift.date.strftime('%m/%d/%Y')
    })
