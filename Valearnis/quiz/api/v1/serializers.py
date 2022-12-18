from rest_framework import serializers

from quiz.models import Question, Option, Quiz


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'

    def validate(self, attrs):
        options = attrs.get('options')
        # check if options are more than 2
        if len(options) < 2:
            raise serializers.ValidationError('At least two options are required')
        # checking if there is at least one correct option
        found_answer = False
        for option in options:
            if 'text' not in option:
                raise serializers.ValidationError('Option text is required')
            if option.get('is_correct'):
                found_answer = True
        if not found_answer:
            raise serializers.ValidationError('At least one correct answer is required')

        if self.context['request'].method == 'PATCH':
            raise serializers.ValidationError('PATCH not allowed, use PUT instead')

        return super().validate(attrs)

    def create(self, validated_data):
        raw_options = validated_data.pop('options')
        quiz = Question.objects.create(**validated_data)
        options = []
        for option in raw_options:
            options.append(Option.objects.create(**option))
        quiz.options.set(options)

        return quiz

    def update(self, instance, validated_data):
        raw_options = validated_data.pop('options')
        instance = super().update(instance, validated_data)
        prev_options = instance.options.all()
        prev_options.delete()
        options = []
        for option in raw_options:
            options.append(Option.objects.create(**option))
        instance.options.set(options)
        return instance


class QuizSerializer(serializers.ModelSerializer):
    answers = serializers.JSONField(write_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    question_count = serializers.IntegerField(label="Question Count", write_only=True, required=False)

    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['user', 'score', 'questions']

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            if 'question_count' in attrs:
                if attrs.get('question_count') < 1:
                    raise serializers.ValidationError('Question count must be greater than 1')
            else:
                raise serializers.ValidationError('Question count is required')
        elif self.context['request'].method == 'PUT':
            if 'answers' in attrs:
                answers = attrs.get('answers')
                if len(answers) < 1:
                    raise serializers.ValidationError('At least one answer is required')
                for answer in answers:
                    if 'question_id' not in answer:
                        raise serializers.ValidationError('Question id is required')
                    if 'options_id' not in answer:
                        raise serializers.ValidationError('Option id is required')
            else:
                raise serializers.ValidationError('Answers are required')
        else:
            raise serializers.ValidationError('Invalid request method')

        return super().validate(attrs)

    def create(self, validated_data):
        question_count = validated_data.pop('question_count')
        questions = Question.objects.order_by('?')[:question_count]
        if questions.count() < question_count:
            raise serializers.ValidationError('Not enough questions available')
        quiz = Quiz.objects.create(user=self.context['request'].user)
        quiz.questions.set(questions)
        return quiz

    def update(self, instance, validated_data):
        user = self.context['request'].user
        answers = validated_data.pop('answers')

        # re-validating the answers
        if instance.user != user:
            raise serializers.ValidationError('You are not allowed to answer this quiz')

        if instance.questions.count() != len(answers):
            raise serializers.ValidationError('Invalid answer count')

        for answer in answers:
            if not instance.questions.filter(id=answer.get('question_id')).exists():
                raise serializers.ValidationError('Invalid question id')

        score = 0
        for answer in answers:
            question = instance.questions.get(id=answer.get('question_id'))
            options = question.options.filter(id__in=answer.get('options_id')).values_list('id', flat=True)
            correct_options = question.options.filter(is_correct=True).values_list('id', flat=True)
            if list(options) == list(correct_options):
                score += 1
        instance.score = score
        instance.save()
        return instance
