from odoo.addons.survey.controllers.main import Survey
from odoo.http import request
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import fields, http


class Surveycontact(Survey):
    @http.route('/survey/submit/<string:survey_token>/<string:answer_token>',
                type='json', auth='public', website=True)
    def survey_submit(self, survey_token, answer_token, **post):
        # print("fgif", post)
        # print("fgi", post[1])

        """ Submit a page from the survey.
        This will take into account the validation errors and store the answers
         to the questions.
        If the time limit is reached, errors will be skipped, answers will be 
        ignored and
        survey state will be forced to 'done'"""
        # Survey Validation
        access_data = self._get_access_data(survey_token, answer_token,
                                            ensure_token=True)
        if access_data['validity_code'] is not True:
            return {'error': access_data['validity_code']}
        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data[
            'answer_sudo']

        if answer_sudo.state == 'done':
            return {'error': 'unauthorized'}

        questions, page_or_question_id = survey_sudo._get_survey_questions(
            answer=answer_sudo,
            page_id=post.get('page_id'),
            question_id=post.get('question_id'))

        if not answer_sudo.test_entry and not survey_sudo._has_attempts_left(
                answer_sudo.partner_id, answer_sudo.email,
                answer_sudo.invite_token):
            # prevent cheating with users creating multiple 'user_input'
            # before their last attempt
            return {'error': 'unauthorized'}

        if answer_sudo.survey_time_limit_reached or \
                answer_sudo.question_time_limit_reached:
            if answer_sudo.question_time_limit_reached:
                time_limit =\
                    survey_sudo.session_question_start_time +\
                    relativedelta(seconds=survey_sudo.session_question_id.
                                  time_limit)
                time_limit += timedelta(seconds=3)
            else:
                time_limit = answer_sudo.start_datetime + timedelta(
                    minutes=survey_sudo.time_limit)
                time_limit += timedelta(seconds=10)
            if fields.Datetime.now() > time_limit:
                # prevent cheating with users blocking the JS timer and taking
                # all their time to answer
                return {'error': 'unauthorized'}

        errors = {}
        # take records from survey.contacts
        records = request.env['survey.contacts'] \
            .search([('question_id', '=', questions.ids)])
        # print(records, "1")
        # print(records.question_id, "1")
        vals = {}
        # Prepare answers / comment by question, validate and save answers
        for question in questions:
            inactive_questions = request.env[
                'survey.question'] if answer_sudo.is_session_answer else answer_sudo._get_inactive_conditional_questions()
            if question in inactive_questions:  # if question is inactive, skip validation and save
                continue
            answer, comment = \
                self._extract_comment_from_answers(question,
                                                   post.get(str(question.id)))
            # print(question.title, "single question")
            # loop in each survey contacts
            for rec in records:
                if question == rec.question_id and rec.contact_fields_id:
                    # print("field =", rec.contact_fields_id.name)
                    # print("answer =", answer)
                    vals[rec.contact_fields_id.name] = answer

            errors.update(question.validate_question(answer, comment))
            if not errors.get(question.id):
                answer_sudo.save_lines(question, answer, comment)
        # print(vals)
        request.env['res.partner'].create(vals)
        if errors and not (
                answer_sudo.survey_time_limit_reached or
                answer_sudo.question_time_limit_reached):
            return {'error': 'validation', 'fields': errors}

        if not answer_sudo.is_session_answer:
            answer_sudo._clear_inactive_conditional_answers()

        if answer_sudo.survey_time_limit_reached or\
                survey_sudo.questions_layout == 'one_page':
            answer_sudo._mark_done()
        elif 'previous_page_id' in post:
            # Go back to specific page using the breadcrumb. Lines are saved
            # and survey continues
            return self._prepare_question_html(survey_sudo, answer_sudo,
                                               **post)
        else:
            vals = {'last_displayed_page_id': page_or_question_id}
            if not answer_sudo.is_session_answer:
                next_page =\
                    survey_sudo._get_next_page_or_question(answer_sudo,
                                                           page_or_question_id)
                if not next_page:
                    answer_sudo._mark_done()

            answer_sudo.write(vals)

        return self._prepare_question_html(survey_sudo, answer_sudo)

    def _extract_comment_from_answers(self, question, answers):
        """ Answers is a custom structure depending of the question type
        that can contain question answers but also comments that need to be
        extracted before validating and saving answers.
        If multiple answers, they are listed in an array, except for matrix
        where answers are structured differently. See input and output for
        more info on data structures.
        :param question: survey.question
        :param answers:
          * question_type: free_text, text_box, numerical_box, date, datetime
            answers is a string containing the value
          * question_type: simple_choice with no comment
            answers is a string containing the value ('question_id_1')
          * question_type: simple_choice with comment
            ['question_id_1', {'comment': str}]
          * question_type: multiple choice
            ['question_id_1', 'question_id_2'] + [{'comment': str}] if holds a
            comment
          * question_type: matrix
            {'matrix_row_id_1': ['question_id_1', 'question_id_2'],
             'matrix_row_id_2': ['question_id_1', 'question_id_2']
            } + {'comment': str} if holds a comment
        :return: tuple(
          same structure without comment,
          extracted comment for given question
        ) """
        comment = None
        answers_no_comment = []
        if answers:
            if question.question_type == 'matrix':
                if 'comment' in answers:
                    comment = answers['comment'].strip()
                    answers.pop('comment')
                answers_no_comment = answers
            else:
                if not isinstance(answers, list):
                    answers = [answers]
                for answer in answers:
                    if isinstance(answer, dict) and 'comment' in answer:
                        comment = answer['comment'].strip()
                    else:
                        answers_no_comment.append(answer)
                if len(answers_no_comment) == 1:
                    answers_no_comment = answers_no_comment[0]
        return answers_no_comment, comment
    