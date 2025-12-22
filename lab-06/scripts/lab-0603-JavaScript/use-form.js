// ЗАДАНИЕ 2: Кастомный хук для управления формой
import { useState, useCallback } from 'react';

const useForm = (initialValues, validateFn = () => ({})) => {
    const [values, setValues] = useState(initialValues);
    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Обновление значения поля
    const handleChange = useCallback((fieldName, value) => {
        setValues(prevValues => ({
            ...prevValues,
            [fieldName]: value
        }));
        
        // Очистка ошибки при изменении
        if (errors[fieldName]) {
            setErrors(prevErrors => ({
                ...prevErrors,
                [fieldName]: ''
            }));
        }
    }, [errors]);

    // Валидация формы
    const validate = useCallback(() => {
        const newErrors = validateFn(values);
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    }, [values, validateFn]);

    // Обработка отправки формы
    const handleSubmit = useCallback(async (onSubmit) => {
        setIsSubmitting(true);
        const isValid = validate();
        
        if (isValid) {
            try {
                await onSubmit(values);
            } catch (error) {
                console.error('Submit error:', error);
            }
        }
        
        setIsSubmitting(false);
        return isValid;
    }, [values, validate]);

    return {
        values,
        errors,
        isSubmitting,
        handleChange,
        handleSubmit,
        setValues,
        validate
    };
};

export default useForm;
