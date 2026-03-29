<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Form;

use App\Entity\ProductGroup;
use App\Entity\Training;
use Symfony\Bridge\Doctrine\Form\Type\EntityType;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\DateTimeType;
use Symfony\Component\Form\Extension\Core\Type\IntegerType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

/**
 * Class TrainingType.
 */
class TrainingType extends AbstractType
{
    /**
     * @param FormBuilderInterface $builder
     * @param array                $options
     */
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder
            ->add('productGroup', EntityType::class, ['class' => ProductGroup::class])
            ->add('status', IntegerType::class)
            ->add('stale', IntegerType::class)
            ->add('scheduledStartDate', DateTimeType::class)
            ->add('estimatedEndDate', DateTimeType::class);
    }

    /**
     * @param OptionsResolver $resolver
     */
    public function configureOptions(OptionsResolver $resolver)
    {
        $resolver->setDefaults(
            [
                'data_class' => Training::class,
                'csrf_protection' => false,
                'allow_extra_fields' => false,
            ]
        );
    }
}
