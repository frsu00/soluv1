from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    codigo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=50)

    def cantidad_productos(self):
        return Producto.objects.filter(categoria=self.id).count()

    def __str__(self):
        return self.nombre

class Localizacion(models.Model):
    distrito = models.CharField(max_length=20)
    provincia = models.CharField(max_length=20)
    departamento = models.CharField(max_length=20)

    def __str__(self):
        return self.distrito


class Producto(models.Model):
    # Relaciones
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey('Colaborador', on_delete=models.SET_NULL, null=True)

    # Atributos
    fecha_creacion = models.DateField(auto_now=True, blank=True, null=True)
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField()
    precio = models.FloatField()
    estado = models.CharField(max_length=3)
    descuento = models.FloatField(default=0)

    def get_precio_final(self):
        return self.precio * (1 - self.descuento)

    def get_discount(self):
        return self.descuento * 100

    def has_discount(self):
        if self.descuento != 0:
            return True

    def sku(self):
        codigo_categoria = self.categoria.codigo.zfill(4)
        codigo_producto = str(self.id).zfill(6)

        return f'{codigo_categoria}-{codigo_producto}'


    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    # Relacionaes
    ubicacion = models.ForeignKey('Localizacion', on_delete=models.SET_NULL, null=True)
    repartidor = models.ForeignKey('Colaborador', on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True)

    # Atributos
    fecha_creacion = models.DateField(auto_now=True, blank=True, null=True)
    estado = models.CharField(max_length=3)
    fechaEntrega = models.DateField(null=True)
    direccion_entrega = models.CharField(max_length=100, blank=True, null=True)
    tarifa = models.FloatField(default=0, blank=True, null=True)

    def __str__(self):
        return f'{self.cliente} - {self.fecha_creacion} - {self.estado}'

    def get_total(self):
        detalles = self.detallepedido_set.all()
        total = 0
        for detalle in detalles:
            total += detalle.get_subtotal()
        total += self.tarifa
        return total


class DetallePedido(models.Model):
    # Relaciones
    pedido = models.ForeignKey('Pedido', on_delete=models.SET_NULL, null=True)
    producto = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True)

    # Atributos
    cantidad = models.IntegerField(null=True)
    subtotal = models.FloatField(null=True)

    def __str__(self):
        return f'{self.pedido.id} - {self.cantidad} x {self.producto.nombre}'

    def get_subtotal(self):
        return self.producto.get_precio_final() * self.cantidad


class Profile(models.Model):
    # Relacion con el modelo User de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Atributos adicionales para el usuario
    documento_identidad = models.CharField(max_length=8)
    fecha_nacimiento = models.DateField()
    estado = models.CharField(max_length=3)
    ## Opciones de genero
    MASCULINO = 'MA'
    FEMENINO = 'FE'
    NO_BINARIO = 'NB'
    GENERO_CHOICES = [
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
        (NO_BINARIO, 'No Binario')
    ]
    genero = models.CharField(max_length=2, choices=GENERO_CHOICES)

    def __str__(self):
        return self.user.get_username()


class Cliente(models.Model):
    # Relacion con el modelo Perfil
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    # Atributos especificos del Cliente
    preferencias = models.ManyToManyField(to='Categoria')
    is_colaborador = models.BooleanField(default=False)

    def __str__(self):
        return f'Cliente: {self.user_profile.user.get_username()}'


class Colaborador(models.Model):
    # Relacion con el modelo Perfil
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    # Atributos especificos del Colaborador
    reputacion = models.FloatField()
    cobertura_entrega = models.ManyToManyField(to='Localizacion')
    is_colaborador = models.BooleanField(default=True)

    # Atributos especificos del proveedor
    ruc = models.CharField(max_length=11)
    razon_social = models.CharField(max_length=20)
    telefono = models.CharField(max_length=9)

    def __str__(self):
        return f'Colaborador: {self.user_profile.user.get_username()}'


class ProductoImage(models.Model):
    product = models.ForeignKey('Producto', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="media/products", null=True, blank=True)
