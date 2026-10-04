from app.core.config import settings

class FeedbackService:
    def generate_feedback(self, pitch_data: dict) -> dict:
        status = pitch_data.get('status')
        f0 = pitch_data.get('f0', 0.0)
        
        if status == 'silence':
            return {
                'message': 'اتكلم أو غني بصوت واضح...',
                'action': 'wait',
                'level': 'info'
            }
            
        if status == 'unvoiced':
            return {
                'message': 'صوتك طالع فيه هواء كتير، وضح النبرة الصدرية.',
                'action': 'add_voice',
                'level': 'warning'
            }
            
        if f0 < settings.TARGET_F0_MIN:
            return {
                'message': f'النبرة واطية بزيادة ({f0:.1f} هرتز)، ارفعها سنة بسيطة.',
                'action': 'raise_pitch',
                'level': 'warning'
            }
            
        if f0 > settings.TARGET_F0_MAX:
            return {
                'message': f'إنت طلعت فوق زون القرار ({f0:.1f} هرتز)، انزل لرنين الصدر بين 80 و 120 هرتز.',
                'action': 'lower_pitch',
                'level': 'warning'
            }
            
        return {
            'message': f'عاش! نبرتك مظبوطة تمام في القرار ({f0:.1f} هرتز).',
            'action': 'hold',
            'level': 'success'
        }

feedback_service = FeedbackService()
