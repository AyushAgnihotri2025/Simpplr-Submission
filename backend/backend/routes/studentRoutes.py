from flask.wrappers import Request
from werkzeug.datastructures import Headers

from backend import app, API_VERSION

from backend.wrappers import auth
from backend.functions import Student

stu = Student()


@app.route(f'/api/{API_VERSION}/get', methods=['GET'])
@auth(check_auth=True)
def get(req: Request, headers: Headers):
    return stu.get(id=req.args.get('id'))


@app.route(f'/api/{API_VERSION}/getAll', methods=['GET'])
@auth(check_auth=True)
def getAll(req: Request, headers: Headers):
    page = req.args.get('page', '')
    count = req.args.get('count', '')

    return stu.getAll(
        class_id=req.args.get('class'),
        page=int(page) if page.isdigit() else 1,
        per_page=min(int(count), 20) if count.isdigit() else 10,
    )


@app.route(f'/api/{API_VERSION}/search', methods=['GET'])
@auth(check_auth=True)
def filterData(req: Request, headers: Headers):
    page = req.args.get('page', '')
    count = req.args.get('count', '')

    return stu.filter(
        name=req.args.get('name'),
        class_name=req.args.get('class_name'),
        class_id=req.args.get('class_id'),
        age=req.args.get('age'),
        max_age=req.args.get('max_age'),
        min_age=req.args.get('min_age'),
        percentage=req.args.get('percentage'),
        min_percentage=req.args.get('min_percentage'),
        max_percentage=req.args.get('max_percentage'),
        grade=req.args.get('grade'),
        stream=req.args.get('stream'),
        total_marks=req.args.get('total_marks'),
        min_marks=req.args.get('min_marks'),
        max_marks=req.args.get('max_marks'),
        total_subjects=req.args.get('total_subjects'),
        min_subjects=req.args.get('min_subjects'),
        max_subjects=req.args.get('max_subjects'),
        page=int(page) if page.isdigit() else 1,
        per_page=min(int(count), 20) if count.isdigit() else 10,
    )


@app.route(f'/api/{API_VERSION}/delete', methods=['DELETE'])
@auth(check_auth=True)
def deleteData(req: Request, headers: Headers):
    return stu.delete(id=req.args.get('id'))


@app.route(f'/api/{API_VERSION}/deleteMany', methods=['POST'])
@auth(check_auth=True)
def deleteMultipleData(req: Request, headers: Headers):
    if req.is_json:
        return stu.delete(id=req.json.get('id', []))
    else:
        return dict(
            success=False,
            message='Invalid Request',
        )


@app.route(f'/api/{API_VERSION}/update', methods=['POST'])
@auth(check_auth=True)
def updateData(req: Request, headers: Headers):
    if req.is_json:
        return stu.update(id=req.args.get('id'), updates=req.json)
    else:
        return dict(
            success=False,
            message='Invalid Request',
        )
