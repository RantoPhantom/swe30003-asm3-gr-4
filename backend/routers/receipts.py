from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..db import Db
import datetime
db = Db("db.sqlite")

router = APIRouter()

class Receipt(BaseModel):
    receipt_id: int
    order_id: int
    invoice_id: int
    total: float
    total_after_tax: float
    payment_method: str
    amount_given: float
    change: float
    date_added: str

class OnlineCheckOutReq(BaseModel):
    invoice_id: int
    order_id: int
    total: float
    total_after_tax: float
    payment_method: str
    amount_given: float
@router.put("/online-check-out", status_code=204, responses={404:{},409:{}})
async def online_check_out(request: OnlineCheckOutReq):
    query: str = '''
    select * from invoices
    where invoice_id =?;
    '''
    res = db.cursor.execute(query, [request.invoice_id]).fetchone()
    if res == None:
        err: str = f"This invoice does not exists: {request.invoice_id}"
        raise HTTPException(status_code=404, detail=err)

    query: str ='''
    select * from receipts
    where invoice_id=?;
    '''
    res = db.cursor.execute(query, [request.invoice_id]).fetchone()
    if res != None:
        err: str = f"This receipt already exists"
        raise HTTPException(status_code=409, detail=err)
    
    query: str ='''
    select * from orders
    where order_id=? AND status='PENDING';
    '''
    res = db.cursor.execute(query, [request.order_id]).fetchone()
    if res == None:
        err: str = f"This Order is already done"
        raise HTTPException(status_code=409, detail=err)

    query: str = '''
    update orders
    set status="COMPLETED"
    where order_id=?;
    '''
    db.cursor.execute(query, [request.order_id])

    change = request.amount_given - request.total_after_tax
    query: str = '''
    select ifnull(max(receipt_id),0) from receipts;
    '''
    max_id = db.cursor.execute(query).fetchone()[0]
    query: str = '''
    insert into receipts
    values(?,?,?,?,?,?,?,?,?);
    '''
    db.cursor.execute(query, (
        max_id + 1,
        request.order_id,
        request.invoice_id,
        request.total,
        request.total_after_tax,
        request.payment_method,
        request.amount_given,
        change,
        datetime.datetime.now().isoformat()
        ))
    db.connection.commit()
    return

class CheckOutReq(BaseModel):
    invoice_id: int
    order_id: int
    table_number: int
    total: float
    total_after_tax: float
    payment_method: str
    amount_given: float
@router.put("/check-out", status_code=204, responses={404:{},409:{}})
async def check_out(request: CheckOutReq):
    query: str = '''
    select * from invoices
    where invoice_id =?;
    '''
    res = db.cursor.execute(query, [request.invoice_id]).fetchone()
    if res == None:
        err: str = f"This invoice does not exists: {request.invoice_id}"
        raise HTTPException(status_code=404, detail=err)

    query: str ='''
    select * from receipts
    where invoice_id=?;
    '''
    res = db.cursor.execute(query, [request.invoice_id]).fetchone()
    if res != None:
        err: str = f"This receipt already exists"
        raise HTTPException(status_code=409, detail=err)
    
    query: str ='''
    select * from orders
    where order_id=? AND status='PENDING';
    '''
    res = db.cursor.execute(query, [request.order_id]).fetchone()
    if res == None:
        err: str = f"This Order is already done"
        raise HTTPException(status_code=409, detail=err)

    query: str ='''
    select order_id from tables
    where order_id=? AND table_number=?;
    '''
    res = db.cursor.execute(query, (request.order_id, request.table_number)).fetchone()
    if res == None:
        err: str = f"This table doesn't have that order: order:{request.order_id} table: {request.table_number}"
        raise HTTPException(status_code=409, detail=err)

    query: str = '''
    update orders
    set status="COMPLETED"
    where order_id=?;
    '''
    db.cursor.execute(query, [request.order_id])

    query: str = '''
    update tables
    set table_status='UNOCCUPIED', order_id=NULL
    where table_number=?
    '''
    db.cursor.execute(query, [request.table_number])

    change = request.amount_given - request.total_after_tax
    query: str = '''
    select ifnull(max(receipt_id),0) from receipts;
    '''
    max_id = db.cursor.execute(query).fetchone()[0]
    query: str = '''
    insert into receipts
    values(?,?,?,?,?,?,?,?,?);
    '''
    db.cursor.execute(query, (
        max_id + 1,
        request.order_id,
        request.invoice_id,
        request.total,
        request.total_after_tax,
        request.payment_method,
        request.amount_given,
        change,
        datetime.datetime.now().isoformat()
        ))
    db.connection.commit()
    return

@router.get("/get-all-receipts", status_code=200)
async def get_all_receipts() -> list[Receipt]:
    response = []
    query: str = '''
    select * from receipts
    '''
    res = db.cursor.execute(query)
    for receipt in res:
        response.append(Receipt(
            receipt_id=receipt[0],
            order_id=receipt[1],
            invoice_id=receipt[2],
            total=receipt[3],
            total_after_tax=receipt[4],
            payment_method=receipt[5],
            amount_given=receipt[6],
            change=receipt[7],
            date_added=receipt[8],
            ))
    return response

@router.get("/get-receipts-from-name/{name}",status_code=200)
async def get_receipts_from_name(name: str) -> list[Receipt]:
    name = f"%{name}%"
    response : list[Receipt] = []
    query: str = '''
    select receipts.* from orders inner join receipts on receipts.order_id=orders.order_id and orders.name like ?
    '''
    res = db.cursor.execute(query, [name]).fetchall()
    for receipts in res:
        response.append(Receipt(
            receipt_id=receipts[0],
            order_id=receipts[1],
            invoice_id=receipts[2],
            total=receipts[3],
            total_after_tax=receipts[4],
            payment_method=receipts[5],
            amount_given=receipts[6],
            change=receipts[7],
            date_added=receipts[8],
            ))
    return response

@router.get("/get-receipts-from-date/{date}",status_code=200)
async def get_receipts_from_date(date: str) -> list[Receipt]:
    date = f"%{date}%"
    response : list[Receipt] = []
    query: str = '''
    select * from receipts
    where date_added like ?
    '''
    res = db.cursor.execute(query, [date]).fetchall()
    for receipts in res:
        response.append(Receipt(
            receipt_id=receipts[0],
            order_id=receipts[1],
            invoice_id=receipts[2],
            total=receipts[3],
            total_after_tax=receipts[4],
            payment_method=receipts[5],
            amount_given=receipts[6],
            change=receipts[7],
            date_added=receipts[8],
            ))
    return response

@router.get("/get-receipts-from-method/{payment_method}",status_code=200)
async def get_receipts_from_payment_method(payment_method: str) -> list[Receipt]:
    payment_method = f"%{payment_method}%"
    response : list[Receipt] = []
    query: str = '''
    select * from receipts
    where payment_method like ?
    '''
    res = db.cursor.execute(query, [payment_method]).fetchall()
    for receipts in res:
        response.append(Receipt(
            receipt_id=receipts[0],
            order_id=receipts[1],
            invoice_id=receipts[2],
            total=receipts[3],
            total_after_tax=receipts[4],
            payment_method=receipts[5],
            amount_given=receipts[6],
            change=receipts[7],
            date_added=receipts[8],
            ))
    return response
