from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Bounty, Submission
from .serializers import BountySerializer, SubmissionSerializer
from .services import evaluate_submission, release_escrow_funds

class BountyViewSet(viewsets.ModelViewSet):
    queryset = Bounty.objects.all()
    serializer_class = BountySerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    # This handles the POST request from your submit.html frontend
    def create(self, request, *args, **kwargs):
        # 1. Create the submission
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()

        bounty = submission.bounty

        try:
            # 2. Trigger the Groq AI
            ai_result = evaluate_submission(
                criteria=bounty.success_criteria, 
                code=submission.code_content
            )
            
            submission.ai_status = ai_result.get('status', 'rejected')
            submission.ai_feedback = ai_result.get('feedback', 'No feedback provided.')
            
            # 3. Trigger PayPal if approved
            # 3. Trigger PayPal if approved
            if clean_status == 'approved':
                print("DEBUGGING: TRIGGERING PAYPAL...")
                
                payout_response = release_escrow_funds(
                    receiver_email=submission.developer_paypal_email,
                    amount=bounty.escrow_amount,
                    reference_id=submission.id
                )
                
                # Print the exact raw payload from PayPal to your terminal
                print(f"RAW PAYPAL RESPONSE: {payout_response}")
                
                # Safely extract the ID regardless of Sandbox response structure
                if 'batch_header' in payout_response:
                    batch_id = payout_response['batch_header'].get('payout_batch_id', 'PAYMENT_SENT_NO_ID')
                else:
                    batch_id = payout_response.get('payout_batch_id', 'PAYMENT_SENT_NO_ID')
                
                submission.payout_batch_id = batch_id
                print(f"DEBUGGING: SAVING BATCH ID '{batch_id}' TO DATABASE.")
            
            # 4. Save all updates to the database
            submission.save()
            
            # 5. Return updated data to the frontend
            response_serializer = self.get_serializer(submission)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # Save the failure status if something crashes (e.g., API limits)
            submission.ai_status = 'rejected'
            submission.ai_feedback = f'System Error: {str(e)}'
            submission.save()
            return Response(
                {'detail': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # I kept your original evaluate action in case you want to manually trigger it later
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
            ai_result = evaluate_submission(
                criteria=bounty.success_criteria, 
                code=submission.code_content
            )
            
            submission.ai_status = ai_result.get('status', 'rejected')
            submission.ai_feedback = ai_result.get('feedback', 'No feedback provided.')
            
            if submission.ai_status == 'approved':
                payout_response = release_escrow_funds(
                    receiver_email=submission.developer_paypal_email,
                    amount=bounty.escrow_amount,
                    reference_id=submission.id
                )
                batch_id = payout_response['batch_header']['payout_batch_id']
                submission.payout_batch_id = batch_id
                
            submission.save()
            
            return Response({
                'status': 'success',
                'ai_feedback': submission.ai_feedback,
                'payout_batch_id': submission.payout_batch_id
            })
            
        except Exception as e:
            return Response(
                {'detail': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def dashboard_view(request):
    return render(request, 'dashboard.html')

def submit_view(request):
    return render(request, 'submit.html')