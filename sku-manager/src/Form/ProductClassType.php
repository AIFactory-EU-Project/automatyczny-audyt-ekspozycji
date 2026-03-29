<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Form;

use App\Entity\ProductClass;
use App\Form\DataTransformer\ProductClassToIntTransformer;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\IntegerType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

/**
 * Class ProductClassType.
 */
class ProductClassType extends AbstractType
{
    private ProductClassToIntTransformer $classToIntTransformer;

    public function __construct(ProductClassToIntTransformer $classToIntTransformer)
    {
        $this->classToIntTransformer = $classToIntTransformer;
    }

    /**
     * @param FormBuilderInterface $builder
     * @param array                $options
     */
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder
            ->add('name', TextType::class)
            ->add('parentClass', IntegerType::class);

        $builder->get('parentClass')->addModelTransformer($this->classToIntTransformer);
    }

    /**
     * @param OptionsResolver $resolver
     */
    public function configureOptions(OptionsResolver $resolver)
    {
        $resolver->setDefaults(
            [
                'data_class' => ProductClass::class,
                'csrf_protection' => false,
                'allow_extra_fields' => false,
            ]
        );
    }
}
