import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-tramites',
  template: \`
    <div>
      <h1>Mis Tramites — Alcaldia de Municipio X</h1>

      <!-- ← VULNERABLE: XSS con bypassSecurityTrustHtml sin DOMPurify -->
      <div [innerHTML]="noticiaHtml"></div>

      <ul>
        <li *ngFor="let t of tramites">{{ t[1] }} — {{ t[3] }}</li>
      </ul>

      <!-- ← VULNERABLE: busqueda de funcionarios visible para ciudadanos -->
      <input [(ngModel)]="busqueda" placeholder="Buscar funcionario..." />
      <button (click)="buscarFuncionario()">Buscar</button>

      <!-- ← VULNERABLE: formulario de pago sin validacion ni enmascarado -->
      <form (ngSubmit)="procesarPago()">
        <input [(ngModel)]="tarjeta" name="tarjeta" placeholder="Numero de tarjeta" type="text" />
        <input [(ngModel)]="cvv" name="cvv" placeholder="CVV" type="text" />
        <input [(ngModel)]="monto" name="monto" placeholder="Monto" type="number" />
        <button type="submit">Pagar Impuesto</button>
      </form>
    </div>
  \`
})
export class TramitesComponent implements OnInit {
  tramites: any[] = [];
  busqueda = '';
  noticiaHtml: SafeHtml = '';
  tarjeta = ''; cvv = ''; monto = 0;

  constructor(private http: HttpClient, private sanitizer: DomSanitizer) {}

  ngOnInit() {
    // ← VULNERABLE: sin interceptor — maneja token manualmente
    const token = localStorage.getItem('token');
    this.http.get<any>(\`\${environment.apiUrl}/tramites/mis-tramites\`,
      { headers: { Authorization: token || '' } }
    ).subscribe({
      next: r => this.tramites = r.tramites,
      error: err => alert(\`Error del servidor: \${JSON.stringify(err.error)}\`)
    });

    this.http.get<any>(\`\${environment.apiUrl}/noticias/ultima\`)
      .subscribe(r => {
        // ← VULNERABLE: bypassea sin sanitizar
        this.noticiaHtml = this.sanitizer.bypassSecurityTrustHtml(r.contenido_html);
      });
  }

  buscarFuncionario() {
    // ← VULNERABLE: sin validacion del input
    const token = localStorage.getItem('token');
    this.http.get(\`\${environment.apiUrl}/intranet/funcionarios?buscar=\${this.busqueda}\`,
      { headers: { Authorization: token || '' } }
    ).subscribe(r => console.log('Funcionarios:', r));
  }

  procesarPago() {
    const token = localStorage.getItem('token');
    this.http.post(\`\${environment.apiUrl}/pago/impuesto\`,
      { numero_tarjeta: this.tarjeta, cvv: this.cvv, monto: this.monto },
      { headers: { Authorization: token || '' } }
    ).subscribe(r => alert(\`Pago OK: \${JSON.stringify(r)}\`));
  }
}
