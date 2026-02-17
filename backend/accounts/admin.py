from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from accounts.models import Company, Profile


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'total_users')
    search_fields = ('name',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

    def total_users(self, obj):
        """Muestra la cantidad de usuarios en la empresa"""
        return obj.profiles.count()
    total_users.short_description = "Total Usuarios"


class ProfileInline(admin.StackedInline):
    """Inline para editar el perfil desde el usuario"""
    model = Profile
    extra = 0
    fields = ('company', 'role')


class UserAdminExtended(BaseUserAdmin):
    """Admin extendido del usuario con el perfil integrado"""
    inlines = [ProfileInline]
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('get_profile_info',)}),
    )
    
    readonly_fields = ('get_profile_info',) + BaseUserAdmin.readonly_fields

    def get_profile_info(self, obj):
        """Muestra información del perfil"""
        try:
            profile = obj.profile
            return f"Empresa: {profile.company.name} | Rol: {profile.get_role_display()}"
        except:
            return "Sin perfil asignado"
    get_profile_info.short_description = "Información del Perfil"


# Desregistrar el UserAdmin original y registrar el personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdminExtended)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'role_display', 'get_email')
    search_fields = ('user__username', 'user__email', 'company__name')
    list_filter = ('company', 'role')
    readonly_fields = ('user',)
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Información de la Empresa', {
            'fields': ('company', 'role')
        }),
    )

    def role_display(self, obj):
        """Muestra el rol de forma legible"""
        return obj.get_role_display()
    role_display.short_description = "Rol"

    def get_email(self, obj):
        """Muestra el email del usuario"""
        return obj.user.email
    get_email.short_description = "Email"

    def save_model(self, request, obj, form, change):
        """Guarda el perfil manteniendo la integridad transaccional"""
        super().save_model(request, obj, form, change)
