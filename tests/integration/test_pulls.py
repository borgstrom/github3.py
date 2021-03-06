# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on PullRequest."""
import github3
from github3 import repos

from .helper import IntegrationHelper


class TestPullRequest(IntegrationHelper):

    """PullRequest integration tests."""

    def get_pull_request(self, repository='sigmavirus24/github3.py', num=235):
        """Get the pull request we wish to use in this test."""
        owner, repo = repository.split('/')
        p = self.gh.pull_request(owner, repo, num)
        assert isinstance(p, github3.pulls.PullRequest)
        return p

    def test_close(self):
        """Show that one can close an open Pull Request."""
        self.basic_login()
        cassette_name = self.cassette_name('close')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(num=241)
            assert p.close() is True

    def test_create_comment(self):
        """Show that a user can create a comment on a PR."""
        self.basic_login()
        cassette_name = self.cassette_name('create_comment')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(num=423)
            comment = p.create_comment('Testing pull request comment')
        assert isinstance(comment, github3.issues.comment.IssueComment)

    def test_commits(self):
        """Show that one can iterate over a PR's commits."""
        cassette_name = self.cassette_name('commits')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            for commit in p.commits():
                assert isinstance(commit, github3.repos.commit.RepoCommit)

    def test_create_review_comment(self):
        """Show that a user can create an in-line reveiw comment on a PR."""
        self.basic_login()
        cassette_name = self.cassette_name('create_review_comment')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(num=286)
            comment = p.create_review_comment(
                body='Testing review comments',
                commit_id='4437428aefdb50913e2acabd0552bd13021dc38f',
                path='github3/pulls.py',
                position=6
            )
        assert isinstance(comment, github3.pulls.ReviewComment)

    def test_diff(self):
        """Show that one can retrieve a bytestring diff of a PR."""
        cassette_name = self.cassette_name('diff')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            diff = p.diff()
            assert isinstance(diff, bytes)
            assert len(diff) > 0

    def test_files(self):
        """Show that one can iterate over a PR's files."""
        cassette_name = self.cassette_name('files')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            for pr_file in p.files():
                assert isinstance(pr_file, github3.pulls.PullFile)

    def test_is_merged(self):
        """Show that one can check if a PR was merged."""
        cassette_name = self.cassette_name('is_merged')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            assert p.is_merged() is True

    def test_issue(self):
        """Show that one can retrieve the associated issue of a PR."""
        cassette_name = self.cassette_name('issue')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            issue = p.issue()
            assert isinstance(issue, github3.issues.Issue)

    def test_issue_comments(self):
        """Show that one can iterate over a PR's issue comments."""
        cassette_name = self.cassette_name('issue_comments')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            for comment in p.issue_comments():
                assert isinstance(comment,
                                  github3.issues.comment.IssueComment)

    def test_patch(self):
        """Show that a user can get the patch from a PR."""
        cassette_name = self.cassette_name('patch')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            patch = p.patch()
            assert isinstance(patch, bytes)
            assert len(patch) > 0

    def test_reopen(self):
        """Show that one can reopen an open Pull Request."""
        self.basic_login()
        cassette_name = self.cassette_name('reopen')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(num=241)
            assert p.reopen() is True

    def test_review_comments(self):
        """Show that one can iterate over a PR's review comments."""
        cassette_name = self.cassette_name('review_comments')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            for comment in p.review_comments():
                assert isinstance(comment, github3.pulls.ReviewComment)

    def test_update(self):
        """Show that one can update an open Pull Request."""
        self.basic_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(num=241)
            assert p.update(p.title) is True

    def test_repository(self):
        """Show that the pull request has the owner repository."""
        self.basic_login()
        cassette_name = self.cassette_name('single')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            assert p.repository == ('sigmavirus24', 'github3.py')


class TestReviewComment(IntegrationHelper):

    """Integration tests for the ReviewComment object."""

    def test_reply(self):
        """Show that a user can reply to an existing ReviewComment."""
        self.basic_login()
        cassette_name = self.cassette_name('reply')
        with self.recorder.use_cassette(cassette_name):
            p = self.gh.pull_request('sigmavirus24', 'github3.py', 286)
            c = next(p.review_comments())
            comment = c.reply('Replying to comments is fun.')
        assert isinstance(comment, github3.pulls.ReviewComment)


class TestPullFile(IntegrationHelper):
    """Integration tests for the PullFile object."""
    def get_pull_request_file(self, owner, repo, pull_number, filename):
        p = self.gh.pull_request(owner, repo, pull_number)

        for pull_file in p.files():
            if pull_file.filename == filename:
                break
        else:
            assert False, "Could not find '{0}'".format(filename)

        return pull_file

    def test_contents(self):
        """Show that a user can retrieve the contents of a PR file."""
        cassette_name = self.cassette_name('contents')
        with self.recorder.use_cassette(cassette_name):
            pull_file = self.get_pull_request_file(
                owner='sigmavirus24', repo='github3.py', pull_number=286,
                filename='github3/pulls.py'
            )
            contents = pull_file.contents()
            assert isinstance(contents, repos.contents.Contents)
            assert contents.decoded != b''
