from rest_framework import serializers
from .models import Bounty, Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        # Moved payout_batch_id here
        read_only_fields = ['ai_status', 'ai_feedback', 'payout_batch_id']

class BountySerializer(serializers.ModelSerializer):
    submissions = SubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Bounty
        fields = '__all__'
        read_only_fields = ['status']