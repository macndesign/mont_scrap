var React = require('react');
var $ = require('jquery');
var CommentList = require('./CommentList.jsx');
var CommentForm = require('./CommentForm.jsx');

module.exports = React.createClass({
    getCookie: function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
    ajaxSetup: function () {
        var csrftoken = this.getCookie('csrftoken');
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    },
    getInitialState: function () {
        return {comments: this.props.comments};
    },
    handleCommentSubmit: function (comment) {
        var comments = this.state.comments;
        comments.push(comment);
        this.setState({comments: comments}, function () {
            this.postComment(comment);
        });
    },
    postComment: function (comment) {
        $.ajax({
            url: this.props.url,
            type: 'POST',
            dataType: 'json',
            data: comment,
            success: function (comments) {
                this.setState({comments: comments});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    getComments: function () {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            success: function (comments) {
                this.setState({comments: comments});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    componentDidMount: function () {
        this.ajaxSetup();
    },
    render: function () {
        return (
            <div>
                <CommentList comments={this.state.comments} />
                <CommentForm url={this.props.url} onCommentSubmit={this.handleCommentSubmit} />
            </div>
        );
    }
});