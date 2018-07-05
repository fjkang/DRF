from rest_framework import serializers

from .models import Question, Choice

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    choices = serializers.HyperlinkedRelatedField(many=True, view_name='choice-detail', read_only=True)
    class Meta:
        fields = ('url', 'id', 'question_text', 'pub_date', 'choices')
        model = Question


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('url', 'id', 'question', 'choice_text', 'votes')
        model = Choice