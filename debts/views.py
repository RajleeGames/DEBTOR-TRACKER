# views.py
# ───────────────────────────────────────────────────────────────────────────
from django.shortcuts           import render, get_object_or_404, redirect
from django.urls                import reverse
from django.contrib             import messages
from django.contrib.auth.views  import LoginView
from django.contrib.auth.decorators import login_required
from django.db.models           import Sum, Case, When, F, Value, DecimalField

from .models    import Debtor, Transaction
from .forms     import DebtorForm, TransactionForm, UserRegisterForm, ProfileUpdateForm

# ─── 1) Custom LoginView ───────────────────────────────────────────────────
class MyLoginView(LoginView):
    template_name = 'debts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('debtor_list')


# ─── 2) Debtor list & summary ──────────────────────────────────────────────
@login_required
def debtor_list(request):
    q = request.GET.get('q', '')

    # Annotate filtered debtors
    debtors = Debtor.objects.filter(name__icontains=q).annotate(
        computed_balance=Sum(
            Case(
                When(transactions__kind='debit',  then=F('transactions__amount')),
                When(transactions__kind='credit', then=-F('transactions__amount')),
                default=Value(0),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )
    ).order_by('name')

    total_balance = sum(d.computed_balance or 0 for d in debtors)

    # For highest/lowest, annotate all
    all_debtors = Debtor.objects.annotate(
        computed_balance=Sum(
            Case(
                When(transactions__kind='debit',  then=F('transactions__amount')),
                When(transactions__kind='credit', then=-F('transactions__amount')),
                default=Value(0),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )
    ).filter(computed_balance__gt=0)

    highest_debtor = all_debtors.order_by('-computed_balance').first()
    lowest_debtor  = all_debtors.order_by('computed_balance').first()

    top5    = all_debtors.order_by('-computed_balance')[:5]
    bottom5 = all_debtors.order_by('computed_balance')[:5]

    return render(request, 'debts/debtor_list.html', {
        'debtors':        debtors,
        'q':              q,
        'total_balance':  total_balance,
        'highest_debtor': highest_debtor,
        'lowest_debtor':  lowest_debtor,
        'top5':           top5,
        'bottom5':        bottom5,
    })


# ─── 3) Detail, add, edit, delete views ────────────────────────────────────
@login_required
def debtor_detail(request, pk):
    debtor = get_object_or_404(Debtor, pk=pk)
    txs    = debtor.transactions.order_by('-timestamp')
    return render(request, 'debts/debtor_detail.html', {'debtor': debtor, 'txs': txs})


@login_required
def debtor_add(request):
    form = DebtorForm(request.POST or None)
    if form.is_valid():
        d = form.save()
        return redirect('debtor_detail', pk=d.pk)
    return render(request, 'debts/form.html', {
        'form':       form,
        'title':      'Add Debtor',
        'cancel_url': reverse('debtor_list'),
    })


@login_required
def debtor_edit(request, pk):
    debtor = get_object_or_404(Debtor, pk=pk)
    form   = DebtorForm(request.POST or None, instance=debtor)
    if form.is_valid():
        form.save()
        return redirect('debtor_detail', pk=pk)
    return render(request, 'debts/form.html', {
        'form':       form,
        'title':      'Edit Debtor',
        'cancel_url': reverse('debtor_detail', args=[pk]),
    })


@login_required
def debtor_delete(request, pk):
    debtor = get_object_or_404(Debtor, pk=pk)
    if request.method == 'POST':
        debtor.delete()
        return redirect('debtor_list')
    return render(request, 'debts/confirm_delete.html', {
        'object': debtor.name,
        'cancel_url': reverse('debtor_detail', args=[pk]),
    })


# ─── 4) Transaction views ─────────────────────────────────────────────────
@login_required
def transaction_add(request, pk):
    debtor = get_object_or_404(Debtor, pk=pk)
    form   = TransactionForm(request.POST or None)
    if form.is_valid():
        tx = form.save(commit=False)
        tx.debtor = debtor
        tx.save()
        return redirect('debtor_detail', pk=pk)
    return render(request, 'debts/form.html', {
        'form':       form,
        'title':      'Add Transaction',
        'cancel_url': reverse('debtor_detail', args=[pk]),
    })


@login_required
def transaction_edit(request, debtor_pk, pk):
    debtor = get_object_or_404(Debtor, pk=debtor_pk)
    tx     = get_object_or_404(Transaction, pk=pk, debtor=debtor)
    form   = TransactionForm(request.POST or None, instance=tx)
    if form.is_valid():
        form.save()
        return redirect('debtor_detail', pk=debtor_pk)
    return render(request, 'debts/form.html', {
        'form':       form,
        'title':      'Edit Transaction',
        'cancel_url': reverse('debtor_detail', args=[debtor_pk]),
    })


@login_required
def transaction_delete(request, debtor_pk, pk):
    debtor = get_object_or_404(Debtor, pk=debtor_pk)
    tx     = get_object_or_404(Transaction, pk=pk, debtor=debtor)
    if request.method == 'POST':
        tx.delete()
        return redirect('debtor_detail', pk=debtor_pk)
    return render(request, 'debts/confirm_delete.html', {
        'object':     f"{tx.get_kind_display()} — Tsh{tx.amount:.2f}",
        'cancel_url': reverse('debtor_detail', args=[debtor_pk]),
    })


# ─── 5) Registration & Profile ────────────────────────────────────────────
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'debts/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your profile was updated.')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'debts/profile.html', {'p_form': p_form})
