<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Form;

use App\Entity\Image;
use App\Form\DataTransformer\ProductToIntTransformer;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\CheckboxType;
use Symfony\Component\Form\Extension\Core\Type\IntegerType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

/**
 * Class ImageType.
 */
class ImageType extends AbstractType
{
    private ProductToIntTransformer $productToIntTransformer;

    public function __construct(ProductToIntTransformer $productToIntTransformer)
    {
        $this->productToIntTransformer = $productToIntTransformer;
    }

    /**
     * @param FormBuilderInterface $builder
     * @param array                $options
     */
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder
            ->add('product', IntegerType::class)
            ->add('main', CheckboxType::class)
            ->add('content', TextType::class)
            ->add('baseFilename', TextType::class);

        $builder->get('product')->addModelTransformer($this->productToIntTransformer);
    }

    /**
     * @param OptionsResolver $resolver
     */
    public function configureOptions(OptionsResolver $resolver)
    {
        $resolver->setDefaults(
            [
                'data_class' => Image::class,
                'csrf_protection' => false,
                'allow_extra_fields' => false,
            ]
        );
    }
}
