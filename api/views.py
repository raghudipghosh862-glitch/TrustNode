from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Bounty, Submission
from .serializers import BountySerializer, SubmissionSerializer
from .services import evaluate_submission
from .services import evaluate_submission, release_escrow_funds

class BountyViewSet(viewsets.ModelViewSet):
    queryset = Bounty.objects.all()
    serializer_class = BountySerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    @action(detail=True, methods=['post'])
    def evaluate(self, request, pk=None):
        submission = self.get_object()
        bounty = submission.bounty
        
        # Prevent re-evaluating if already approved
        if submission.ai_status == 'approved':
            return Response(
                {'detail': 'This submission has already been approved and paid.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Trigger the Groq AI using the service we created
            ai_result = evaluate_submission(
                criteria=bounty.success_criteria, 
                code=submission.code_content
            )
            
            # Parse the JSON response from Groq and update the database
            submission.ai_status = ai_result.get('status', 'rejected')
            submission.ai_feedback = ai_result.get('feedback', 'No feedback provided.')
            submission.save()
            
            if submission.ai_status == 'approved':
                payout_response = release_escrow_funds(
                    receiver_email=submission.developer_paypal_email,
                    amount=bounty.escrow_amount,
                    reference_id=submission.id
                )
                return Response({
                    'status': 'success',
                    'ai_feedback': submission.ai_feedback,
                    'payout_batch_id': payout_response['batch_header']['payout_batch_id']
                })
            
            return Response({
                'ai_status': submission.ai_status,
                'ai_feedback': submission.ai_feedback
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
def dashboard_view(request):
    return render(request, 'dashboard.html')
def submit_view(request):
    return render(request, 'submit.html')
